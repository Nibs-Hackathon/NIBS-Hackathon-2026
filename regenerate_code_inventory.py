#!/usr/bin/env python3
"""
Regenerate Project_Code_Inventory_By_Folder as one markdown file per source folder.

Layout mirrors backend/ and frontend/:
  Project_Code_Inventory_By_Folder/backend/api/adapters/FILES.md
contains only the source files directly inside backend/api/adapters/.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "Project_Code_Inventory_By_Folder"
UPDATED_PATH = ROOT / "Project_Code_Inventory_Updated.md"
INVENTORY_NAME = "FILES.md"

AREAS = ("backend", "frontend")

SKIP_DIR_NAMES = {
    ".git", ".cursor", ".vercel", ".venv", "venv",
    "node_modules", "dist", "dist-ssr", "build", "coverage",
    "__pycache__", "test-results", "playwright-report", "blob-report",
    "Project_Code_Inventory_By_Folder",
}

SKIP_FILE_NAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Project_Code_Inventory_Updated.md",
    "regenerate_code_inventory.py",
}

SKIP_SUFFIXES = {
    ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", ".bin",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".zip", ".gz", ".whl", ".db", ".sqlite", ".sqlite3", ".map",
}

LANG = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript",
    ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript",
    ".css": "css", ".scss": "scss", ".html": "html", ".json": "json",
    ".md": "markdown", ".toml": "toml", ".yml": "yaml", ".yaml": "yaml",
    ".txt": "text", ".sql": "sql", ".sh": "bash", ".ps1": "powershell",
}


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S UTC")


def is_secret_env(path: Path) -> bool:
    name = path.name
    if name == ".env.example":
        return False
    return name == ".env" or name.startswith(".env.")


def should_skip_dir(path: Path) -> bool:
    return path.name in SKIP_DIR_NAMES or path.name.endswith(".egg-info")


def should_include_file(path: Path) -> bool:
    if not path.is_file() or path.name in SKIP_FILE_NAMES or is_secret_env(path):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    if "Project_Code_Inventory" in path.parts:
        return False
    try:
        if b"\x00" in path.read_bytes()[:8000]:
            return False
    except OSError:
        return False
    return True


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fence_lang(path: Path) -> str:
    return LANG.get(path.suffix.lower(), "")


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def render_file_section(path: Path) -> str:
    code = read_text(path)
    lang = fence_lang(path)
    opener = f"```{lang}" if lang else "```"
    folder = path.parent.relative_to(ROOT).as_posix()
    return (
        f"## {rel(path)}\n\n"
        f"**Folder path:** `{folder}`\n\n"
        f"**File path:** `{rel(path)}`\n\n"
        f"{opener}\n"
        f"{code.rstrip()}\n"
        f"```\n"
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def clear_out_dir() -> None:
    if OUT_DIR.exists():
        for path in sorted(OUT_DIR.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                try:
                    path.rmdir()
                except OSError:
                    pass
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def walk_area(area: Path) -> dict[Path, list[Path]]:
    """Map each directory under area -> files directly in that directory."""
    by_dir: dict[Path, list[Path]] = defaultdict(list)
    stack = [area]
    while stack:
        current = stack.pop()
        if current != area and should_skip_dir(current):
            continue
        try:
            entries = list(current.iterdir())
        except OSError:
            continue
        for entry in sorted(entries):
            if entry.is_dir():
                if not should_skip_dir(entry):
                    stack.append(entry)
            elif should_include_file(entry):
                by_dir[current].append(entry)
    return by_dir


def inventory_markdown(folder_rel: str, files: list[Path]) -> str:
    files = sorted(files, key=lambda p: p.name.lower())
    parts = [
        f"# Folder: {folder_rel} Code Inventory\n",
        f"Generated: {stamp()}\n",
        f"**Folder path:** `{folder_rel}`\n",
        f"Contains {len(files)} project file(s) directly in this folder "
        f"(nested folders have their own inventory files).\n",
    ]
    for path in files:
        parts.append(render_file_section(path))
    return "\n".join(parts)


def folder_readme(folder_rel: str, child_dirs: list[str], file_count: int, has_files: bool) -> str:
    parts = [
        f"# {folder_rel}\n",
        f"Generated: {stamp()}\n",
        f"**Folder path:** `{folder_rel}`\n",
    ]
    if has_files:
        parts.append(f"- [Source files in this folder]({INVENTORY_NAME}) ({file_count} files)\n")
    if child_dirs:
        parts.append("## Subfolders\n")
        for child in child_dirs:
            name = child.split("/")[-1]
            parts.append(f"- [{name}]({name}/README.md)")
    return "\n".join(parts) + "\n"


def main() -> None:
    clear_out_dir()

    area_stats: list[tuple[str, int, int]] = []
    all_folder_links: list[tuple[str, str, int]] = []

    for area_name in AREAS:
        area = ROOT / area_name
        if not area.exists():
            continue
        by_dir = walk_area(area)

        # Include ancestor directories so README trees are complete
        dirs = set(by_dir.keys())
        for d in list(by_dir.keys()):
            cur = d
            while True:
                dirs.add(cur)
                if cur == area:
                    break
                cur = cur.parent

        folder_count = 0
        file_count = 0

        for directory in sorted(dirs, key=lambda p: rel(p).lower()):
            folder_rel = rel(directory)
            out_folder = OUT_DIR / folder_rel
            out_folder.mkdir(parents=True, exist_ok=True)

            files = by_dir.get(directory, [])
            has_files = bool(files)
            if has_files:
                write(out_folder / INVENTORY_NAME, inventory_markdown(folder_rel, files))
                file_count += len(files)
                folder_count += 1
                link = f"{folder_rel}/{INVENTORY_NAME}"
                all_folder_links.append((folder_rel, link, len(files)))

            child_dirs = sorted(
                {
                    rel(child)
                    for child in dirs
                    if child.parent == directory
                },
                key=str.lower,
            )
            # child display names relative for links
            child_names = [c.split("/")[-1] for c in child_dirs]
            write(
                out_folder / "README.md",
                folder_readme(folder_rel, child_names, len(files), has_files),
            )

        area_stats.append((area_name, file_count, folder_count))

    # Top README
    top = [
        "# Project Code Inventory by Folder\n",
        f"Generated: {stamp()}\n",
        "Each source folder under `backend/` and `frontend/` has a mirrored inventory folder.\n",
        f"Open `{INVENTORY_NAME}` inside a mirrored folder for that folder's source files "
        "(with full file paths). Nested folders are inventoried separately.\n",
        "## Project areas\n",
    ]
    for name, files, folders in area_stats:
        top.append(
            f"- [{name}]({name}/README.md) — {files} files across {folders} folder inventories"
        )
    top.append("\n## All folder inventories\n")
    for folder_rel, link, count in sorted(all_folder_links, key=lambda x: x[0].lower()):
        top.append(f"- [`{folder_rel}`]({link}) ({count} files)")
    write(OUT_DIR / "README.md", "\n".join(top) + "\n")

    # Replace monolith with an index pointing at the split inventories
    updated = [
        "# Project Code Inventory (Updated)\n",
        f"Generated: {stamp()}\n",
        "This inventory is split by folder. Do not keep a single monolith dump.\n",
        f"See **[Project_Code_Inventory_By_Folder/README.md](Project_Code_Inventory_By_Folder/README.md)**.\n",
        "## Layout\n",
        f"- Mirror of `backend/` and `frontend/`\n"
        f"- Each folder with source files has `{INVENTORY_NAME}` containing those files\n"
        f"- Each folder has `README.md` linking to `{INVENTORY_NAME}` and subfolders\n",
        "## Areas\n",
    ]
    for name, files, folders in area_stats:
        updated.append(
            f"- [{name}](Project_Code_Inventory_By_Folder/{name}/README.md) "
            f"({files} files / {folders} folders)"
        )
    updated.append("\n## Folder index\n")
    for folder_rel, link, count in sorted(all_folder_links, key=lambda x: x[0].lower()):
        updated.append(
            f"- [`{folder_rel}`](Project_Code_Inventory_By_Folder/{link}) ({count} files)"
        )
    write(UPDATED_PATH, "\n".join(updated) + "\n")

    print(f"Wrote {OUT_DIR}")
    print(f"Wrote index {UPDATED_PATH}")
    print(f"Areas: {area_stats}")
    print(f"Folder inventories: {len(all_folder_links)}")


if __name__ == "__main__":
    main()
