import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )


from rag.ingestion import KnowledgeIngestion



engine = KnowledgeIngestion()


count = engine.ingest_folder(
    "docs"
)


print(
    f"Indexed {count} chunks"
)