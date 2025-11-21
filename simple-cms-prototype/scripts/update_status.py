"""
Deprecation wrapper for update_status.py

This script was replaced by `scripts/sync_status.py` (which updates both JSON
and the markdown header). Keep this wrapper to preserve the old CLI but it
forwards the call to `sync_status.py`.
"""
import sys
import subprocess
import os

if len(sys.argv) < 3:
    print("Usage: python scripts/update_status.py <article_id> <new_status>")
    sys.exit(1)

# Forward to sync_status.py for unified behavior
args = [sys.executable, os.path.join(os.path.dirname(__file__), "sync_status.py")] + sys.argv[1:]
try:
    rc = subprocess.call(args)
    sys.exit(rc)
except Exception as e:
    print(f"Failed to forward to sync_status.py: {e}")
    sys.exit(2)
