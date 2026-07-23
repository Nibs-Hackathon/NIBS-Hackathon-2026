class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store


    def retrieve(self, query):

        db = self.vector_store.get()

        if db is None:
            return []


        return db.similarity_search(
            query
        )