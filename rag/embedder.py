from langchain_huggingface import HuggingFaceEmbeddings


class Embedder:


    def __init__(self):

        self.model = HuggingFaceEmbeddings(

            model_name=
            "sentence-transformers/all-MiniLM-L6-v2"

        )


    def get_model(self):

        return self.model