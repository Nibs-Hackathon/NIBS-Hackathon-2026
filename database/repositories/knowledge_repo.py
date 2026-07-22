from database.models import KnowledgeDB

class KnowledgeRepository:

    def __init__(self, session):
        self.session = session

    def create(
            self,
            knowledge
    ):
        self.session.add(
            knowledge
        )
        self.session.commit()

        self.session.refresh(
            knowledge
        )
        return knowledge

    def create_many(
            self,
            documents
    ):
        self.session.add_all(
            documents
        )
        self.session.commit()
        return documents

    def similarity_search(
            self,
            embedding,
            limit = 5
    ):

        results = (
            self.session
            .query(KnowledgeDB)

            .order_by(
                KnowledgeDB.embedding.cosine_distance(
                    embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results

    def get_all(self):
        return (
            self.session
            .query(
                KnowledgeDB
            ).delete()
        )
    
        self.session.commit()