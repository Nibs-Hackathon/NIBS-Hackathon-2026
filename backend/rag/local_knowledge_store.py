"""Always-available lexical retrieval over the checked-in refinery corpus."""

from __future__ import annotations

import re
from pathlib import Path

from langchain_core.documents import Document


BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_DIR = BACKEND_ROOT / "knowledge_docs"
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,}", re.IGNORECASE)
STOP_WORDS = {
    "about", "after", "also", "and", "are", "asset", "for", "from", "have",
    "into", "not", "of", "on", "or", "refinery", "that", "the", "their",
    "this", "to", "what", "when", "where", "which", "with",
}


def _normalize_token(token: str) -> str:
    """Apply conservative stemming for industrial nouns used in headings."""
    normalized = token.casefold()
    if len(normalized) > 5 and normalized.endswith("ies"):
        return f"{normalized[:-3]}y"
    if len(normalized) > 4 and normalized.endswith("s") and not normalized.endswith("ss"):
        return normalized[:-1]
    return normalized


def _tokens(value: str) -> set[str]:
    tokens = {_normalize_token(token) for token in TOKEN_RE.findall(value or "")}
    return {token for token in tokens if token not in STOP_WORDS}


def _document_summary(text: str) -> str:
    """Return the first useful prose paragraph without Markdown syntax."""
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip() and not paragraph.lstrip().startswith("#")
    ]
    if not paragraphs:
        return ""
    summary = re.sub(r"\s+", " ", paragraphs[0])
    return summary[:237].rstrip() + ("..." if len(summary) > 237 else "")


def _document_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def _split_markdown(text: str, source: Path, target_size: int = 1200) -> list[Document]:
    """Split Markdown by headings, then bound oversized sections."""
    sections: list[tuple[str, list[str]]] = []
    heading = source.stem.replace("_", " ").replace("-", " ").title()
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            if body:
                sections.append((heading, body))
            heading = line.lstrip("#").strip() or heading
            body = []
        else:
            body.append(line)
    if body:
        sections.append((heading, body))

    documents: list[Document] = []
    source_label = f"knowledge_docs/{source.name}"
    for section, lines in sections:
        paragraphs = [part.strip() for part in "\n".join(lines).split("\n\n") if part.strip()]
        chunk = ""
        for paragraph in paragraphs:
            candidate = f"{chunk}\n\n{paragraph}".strip()
            if chunk and len(candidate) > target_size:
                documents.append(Document(
                    page_content=f"{section}\n\n{chunk}",
                    metadata={"source": source_label, "section": section},
                ))
                chunk = paragraph
            else:
                chunk = candidate
        if chunk:
            documents.append(Document(
                page_content=f"{section}\n\n{chunk}",
                metadata={"source": source_label, "section": section},
            ))
    return documents


class LocalKnowledgeStore:
    """Small deterministic search index used when vector retrieval is empty."""

    def __init__(self, folder: str | Path = DEFAULT_KNOWLEDGE_DIR):
        self.folder = Path(folder)
        self.documents = self._load()

    def _load(self) -> list[Document]:
        documents: list[Document] = []
        if not self.folder.exists():
            return documents
        for path in sorted(self.folder.rglob("*")):
            if path.suffix.casefold() not in {".md", ".txt"}:
                continue
            documents.extend(_split_markdown(path.read_text(encoding="utf-8"), path))
        return documents

    def count(self) -> int:
        return len(self.documents)

    def catalog(self) -> list[dict[str, object]]:
        """Describe source documents separately from their retrieval chunks."""
        entries: list[dict[str, object]] = []
        if not self.folder.exists():
            return entries
        for path in sorted(self.folder.rglob("*")):
            if path.suffix.casefold() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            sections = [
                line.lstrip("#").strip()
                for line in text.splitlines()
                if line.startswith("## ") and line.lstrip("#").strip()
            ]
            entries.append({
                "id": path.stem,
                "title": _document_title(text, path),
                "filename": path.name,
                "source": f"knowledge_docs/{path.name}",
                "summary": _document_summary(text),
                "sections": sections,
                "section_count": len(sections),
            })
        return entries

    def similarity_search(self, query: str, k: int = 5) -> list[Document]:
        query_tokens = _tokens(query)
        normalized_query = " ".join(TOKEN_RE.findall(query.casefold()))
        ranked = []
        for index, document in enumerate(self.documents):
            metadata = document.metadata or {}
            source_text = f"{Path(str(metadata.get('source', ''))).stem} {metadata.get('section', '')}"
            title_tokens = _tokens(source_text)
            content_tokens = _tokens(document.page_content)
            overlap = query_tokens & content_tokens
            title_overlap = query_tokens & title_tokens
            if query_tokens and not overlap and not title_overlap:
                continue
            score = len(overlap) + len(title_overlap) * 3
            if normalized_query and normalized_query in document.page_content.casefold():
                score += 5
            ranked.append((score, -index, document))
        ranked.sort(reverse=True, key=lambda row: (row[0], row[1]))
        return [row[2] for row in ranked[:k]]


class HybridKnowledgeStore:
    """Prefer configured vector search, falling back to the local corpus."""

    def __init__(self, primary=None, fallback=None):
        self.primary = primary
        self.fallback = fallback or LocalKnowledgeStore()

    def count(self) -> int:
        primary_count = 0
        if self.primary is not None and hasattr(self.primary, "count"):
            try:
                primary_count = int(self.primary.count())
            except Exception:
                primary_count = 0
        return primary_count or self.fallback.count()

    def similarity_search(self, query: str, k: int = 5) -> list[Document]:
        if self.primary is not None:
            try:
                results = self.primary.similarity_search(query, k=k)
                if results:
                    return results
            except Exception:
                pass
        return self.fallback.similarity_search(query, k=k)
