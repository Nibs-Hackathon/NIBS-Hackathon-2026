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