"""Build the Neon/pgvector knowledge index used by the Streamlit UI."""

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )


from rag.ingestion import KnowledgeIngestion


def parse_args():
    parser = argparse.ArgumentParser(
        description="Index PDF knowledge documents into the configured Neon database."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=ROOT_DIR / "docs",
        help="Directory containing PDF source documents (default: ./docs).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing knowledge chunks before indexing. Use for a clean rebuild.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        raise SystemExit(f"Documents directory does not exist: {docs_dir}")

    engine = KnowledgeIngestion()
    if args.replace:
        deleted = engine.vector_store.clear()
        print(f"Removed {deleted} existing knowledge chunk(s).")

    count = engine.ingest_folder(docs_dir)
    total = engine.vector_store.count()
    print(f"Indexed {count} chunk(s). Neon now contains {total} searchable chunk(s).")


if __name__ == "__main__":
    main()
