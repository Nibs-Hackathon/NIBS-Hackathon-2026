
"""Debug script to check Gemini key loading."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from services.llm import LLMManager

print("\n" + "="*60)
print("🔑 DEBUG: Gemini Key Loading")
print("="*60 + "\n")

# Load keys
llm = LLMManager()

print(f"📊 Model: {llm.model_name}")
print(f"📊 Total Keys Found: {len(llm.keys)}")
print(f"📊 Current Key Index: {llm.current_key_index + 1}\n")

print("📋 Key List:")
for i, key in enumerate(llm.keys):
    print(f"  {i+1}. {key[:8]}...{key[-4:]}")

print("\n📊 Key Status:")
status = llm.get_key_status()
for k in status["keys"]:
    print(f"  Key {k['index']}: {k['status']} | Success Rate: {k['success_rate']} | Requests: {k['total_requests']}")

print(f"\n📊 Summary:")
print(f"  Active Keys: {status['summary']['active_keys']}")
print(f"  Available Keys: {status['summary']['available_keys']}")
print(f"  Total Requests: {status['summary']['total_requests']}")

print("\n" + "="*60)