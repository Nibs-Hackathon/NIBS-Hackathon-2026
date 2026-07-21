import faiss

from langchain_community.vectorstores import FAISS


class VectorStore:


    def __init__(self, embeddings):

        self.embeddings = embeddings

        self.db = None



    def create(self, documents):

        self.db = FAISS.from_documents(

            documents,

            self.embeddings

        )



    def save(self, path):

        self.db.save_local(path)



    def load(self, path):

        self.db = FAISS.load_local(

            path,

            self.embeddings,

            allow_dangerous_deserialization=True

        )


    def get(self):

        return self.db