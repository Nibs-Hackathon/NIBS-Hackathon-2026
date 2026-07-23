import httpx
from huggingface_hub import close_session, set_client_factory
from langchain_huggingface import HuggingFaceEmbeddings

from services.llm import _has_invalid_gemini_proxy


def _configure_huggingface_transport() -> None:
    """Keep the embedding download client off the known dead local proxy."""
    if not _has_invalid_gemini_proxy():
        return

    # This changes only huggingface_hub's own HTTP client. It does not mutate
    # process environment variables or alter RAG retrieval behavior.
    set_client_factory(lambda: httpx.Client(trust_env=False))
    close_session()


class Embedder:


    def __init__(self):

        _configure_huggingface_transport()

        self.model = HuggingFaceEmbeddings(

            model_name=
            "sentence-transformers/all-MiniLM-L6-v2"

        )


    def get_model(self):

        return self.model
