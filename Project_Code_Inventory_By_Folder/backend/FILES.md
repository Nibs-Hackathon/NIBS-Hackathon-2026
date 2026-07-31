# Folder: backend Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend`

Contains 5 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/.env.example

**Folder path:** `backend`

**File path:** `backend/.env.example`

```
# Configure keys from separate Google projects to gain independent quota pools.
# Comma-separated pools rotate for both Gemini chat and Gemini embeddings.
GEMINI_API_KEYS=replace-with-key-1,replace-with-key-2

# Alternatively, use individually named keys.
# GEMINI_API_KEY_1=replace-with-key-1
# GEMINI_API_KEY_2=replace-with-key-2

# Optional model override.
# GEMINI_MODEL=gemini-3.5-flash-lite

# PostgreSQL. Replace every placeholder locally; never commit the real URL.
# DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/rigos
```

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

```text
# ============================================
# CORE FRAMEWORKS
# ============================================
fastapi
uvicorn
pydantic
python-dotenv

# ============================================
# DATABASE
# ============================================
SQLAlchemy
alembic
psycopg2-binary
pgvector

# ============================================
# AI & GEMINI
# ============================================
google-generativeai
langchain-google-genai
langchain-community
langchain-huggingface
langchain-text-splitters

# ============================================
# EMBEDDINGS & VECTORS
# ============================================
sentence-transformers
faiss-cpu

# ============================================
# RAG & PDF PROCESSING
# ============================================
pypdf

# ============================================
# UTILITIES
# ============================================
websockets
python-multipart
requests
pandas
plotly

# ============================================
# LOGGING
# ============================================
loguru
```

## backend/run.py

**Folder path:** `backend`

**File path:** `backend/run.py`

```python
import uvicorn
import os

if __name__ == "__main__":
    # Railway provides PORT at runtime; 8080 remains the local and platform default.
    # Reload is opt-in so the production process starts exactly once.
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
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
