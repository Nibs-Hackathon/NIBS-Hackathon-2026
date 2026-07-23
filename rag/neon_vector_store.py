from sqlalchemy import text
from langchain_core.documents import Document

from database.connection import get_session
from database.models import KnowledgeDB
from uuid import uuid4


class NeonVectorStore:


    def __init__(self, embeddings):

        self.embeddings = embeddings


    def create(self, documents):

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



    def similarity_search(
        self,
        query,
        k=5
    ):

        session = get_session()

        try:

            vector = (
                self.embeddings
                .embed_query(query)
            )


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
