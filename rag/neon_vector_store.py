from sqlalchemy import text
from langchain_core.documents import Document

from database.connection import get_session
from database.models import KnowledgeDB
from uuid import uuid4


class NeonVectorStore:

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self._db = None  # For compatibility with FAISS pattern

    def create(self, documents):
        """Create the vector store from a list of documents."""
        session = get_session()
        try:
            for doc in documents:
                vector = (
                    self.embeddings
                    .embed_query(
                        doc.page_content
                    )
                )

                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get(
                        "source",
                        "unknown"
                    ),
                    embedding=vector
                )

                session.add(row)

            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def add_documents(self, documents):
        """Add documents to an existing vector store (incremental)."""
        session = get_session()
        try:
            for doc in documents:
                vector = self.embeddings.embed_query(doc.page_content)
                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                    embedding=vector
                )
                session.add(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def clear(self):
        """Remove all indexed chunks from the active knowledge database."""
        session = get_session()
        try:
            deleted = session.query(KnowledgeDB).delete()
            session.commit()
            return deleted
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def count(self):
        """Return the number of searchable chunks currently stored in Neon."""
        session = get_session()
        try:
            return session.query(KnowledgeDB).count()
        finally:
            session.close()

    def similarity_search(self, query, k=5):
        """Search by query string (generates embedding internally)."""
        session = get_session()
        try:
            vector = self.embeddings.embed_query(query)

            results = session.execute(
                text(
                    """
                    SELECT
                        content,
                        source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                    """
                ),
                {
                    "vector": str(vector),
                    "limit": k
                }
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )

            return documents

        finally:
            session.close()

    # ✅ NEW: Search by pre-computed embedding vector
    def similarity_search_by_vector(self, embedding, k=5):
        """Search by embedding vector (for use with pre-computed embeddings)."""
        session = get_session()
        try:
            results = session.execute(
                text(
                    """
                    SELECT
                        content,
                        source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                    """
                ),
                {
                    "vector": str(embedding),
                    "limit": k
                }
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )

            return documents

        finally:
            session.close()

    # ✅ NEW: Get method for Retriever compatibility
    def get(self):
        """Return self for compatibility with Retriever."""
        return self

    # ✅ NEW: Alias for backward compatibility with FAISS pattern
    def as_retriever(self, search_kwargs=None):
        """Return a retriever interface."""
        from rag.retriever import Retriever
        return Retriever(self)