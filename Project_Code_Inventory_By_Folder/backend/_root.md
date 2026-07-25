# Folder: backend root files Code Inventory

Generated: 2026-07-25T06:14:25 UTC

Contains 4 project files.

## backend/fix_imports.py

**Folder path:** `backend`

**File path:** `backend/fix_imports.py`

```python
"""Fix import paths in adapters."""

import os
import re
from pathlib import Path

# ✅ Use absolute path
ADAPTERS_DIR = Path(__file__).resolve().parent / "api" / "adapters"

print(f"📁 Looking for adapters in: {ADAPTERS_DIR}")

if not ADAPTERS_DIR.exists():
    print(f"❌ Directory not found: {ADAPTERS_DIR}")
    print("Creating directory...")
    ADAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {ADAPTERS_DIR}")
    print("⚠️ Copy adapter files from original project first!")
    exit()

# Map of old imports to new imports
import_map = {
    "from services.runtime import kernel": "from services.runtime import runtime",
    "from services.runtime import simulator": "from services.runtime import runtime",
    "from services.runtime import get_kernel": "from services.runtime import runtime",
    "from app.frontend_services": "from api.adapters",
}

files_fixed = 0
files_skipped = 0

for filename in os.listdir(ADAPTERS_DIR):
    if not filename.endswith('.py'):
        continue
    
    filepath = ADAPTERS_DIR / filename
    modified = False
    
    try:
        # ✅ Use utf-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # ✅ Fallback to latin-1 if utf-8 fails
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ Could not read {filename}: {e}")
            continue
    
    # Replace imports
    for old, new in import_map.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    # Also fix: from services.runtime import kernel → from services.runtime import runtime
    if "from services.runtime import kernel" in content:
        content = content.replace("from services.runtime import kernel", "from services.runtime import runtime")
        modified = True
    
    # Fix: kernel. → runtime.kernel.
    if "kernel." in content and "runtime.kernel" not in content:
        # Only replace if kernel is imported from runtime
        if "from services.runtime import runtime" in content:
            content = content.replace("kernel.", "runtime.kernel.")
            modified = True
    
    if modified:
        # ✅ Write with utf-8 encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filename}")
        files_fixed += 1
    else:
        print(f"⏭️ Skipped: {filename}")
        files_skipped += 1

print(f"\n📊 Summary: {files_fixed} files fixed, {files_skipped} files skipped")
```

## backend/requirements.txt

**Folder path:** `backend`

**File path:** `backend/requirements.txt`

```
# UI
streamlit
# API
fastapi
uvicorn
# Database
sqlalchemy
psycopg2-binary
pgvector
# Environment / config
python-dotenv
# Validation
pydantic
# Logging
loguru
agno
llama-index
# Vector databases
chromadb
# Embeddings
sentence-transformers
# Google Gemini
google-generativeai
langchain-google-genai
# OpenAI fallback
openai
langchain-openai
# LangChain core
langchain
langchain-community
langchain-huggingface
# PDF loading
pypdf
# FAISS vector store
faiss-cpu
# Utilities
uuid64
streamlit
plotly
pandas
python-dotenv
requests
sqlalchemy
psycopg2-binary
pgvector
langchain
langchain-community
langchain-google-genai
sentence-transformers
faiss-cpu
pypdf
# Streamlit UI and domain models
streamlit==1.59.2
pydantic==2.13.4
python-dotenv==1.2.2
# PostgreSQL persistence
SQLAlchemy==2.0.51
alembic==1.18.5
psycopg2-binary==2.9.12
pgvector==0.5.0
# Retrieval-augmented knowledge agent
langchain-community==0.4.2
langchain-google-genai==4.2.7
langchain-huggingface==1.2.2
langchain-text-splitters==1.1.2
sentence-transformers==5.6.0
transformers==5.14.1
torch==2.13.0
faiss-cpu==1.14.3
pypdf==6.14.2
alembic
torchvision
```

## backend/run.py

**Folder path:** `backend`

**File path:** `backend/run.py`

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
```

## backend/test_db.py

**Folder path:** `backend`

**File path:** `backend/test_db.py`

```python
"""Check if tables exist in database."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import engine
from sqlalchemy import inspect, text

print("=" * 50)
print("🔍 Checking database tables")
print("=" * 50)

# Test connection first
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("✅ Connected to:", result.fetchone()[0][:50])
        result = conn.execute(text("SELECT current_database(), current_user"))
        db, user = result.fetchone()
        print(f"✅ Database: {db}, User: {user}")
except Exception as e:
    print("❌ Connection failed:", e)
    sys.exit(1)

# Check if vector extension exists
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        if result.fetchone():
            print("✅ pgvector extension: INSTALLED")
        else:
            print("❌ pgvector extension: NOT INSTALLED")
except Exception as e:
    print("⚠️ Could not check pgvector:", e)

# List all tables
print("\n📊 Tables in database:")
inspector = inspect(engine)
tables = inspector.get_table_names()

if tables:
    print(f"   Found {len(tables)} table(s):")
    for t in sorted(tables):
        # Get column count for each table
        columns = inspector.get_columns(t)
        print(f"   - {t} ({len(columns)} columns)")
else:
    print("   ❌ No tables found!")

# Check specific tables we need
print("\n🔍 Checking required tables:")
required_tables = ['assets', 'telemetry', 'incidents', 'agent_execution', 'execution_reports', 'knowledge']

for table in required_tables:
    if table in tables:
        print(f"   ✅ {table}: EXISTS")
    else:
        print(f"   ❌ {table}: MISSING")

print("\n" + "=" * 50)
```
