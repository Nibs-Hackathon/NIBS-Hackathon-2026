class Retriever:


    def __init__(self, vector_store):

        self.db = vector_store



    def retrieve(self, query, k=3):

        results = self.db.similarity_search(

            query,

            k=k

        )

        return results