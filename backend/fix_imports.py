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