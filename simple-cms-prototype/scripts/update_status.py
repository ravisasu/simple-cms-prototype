"""
Deprecation wrapper for update_status.py

This script was replaced by `scripts/sync_status.py` (which updates both JSON
and the markdown header). Keep this wrapper to preserve the old CLI but it
forwards the call to `sync_status.py`.
"""
import sys
import subprocess
import sys

def main():
    print("Deprecated: 'update_status.py' has been retired. Use 'scripts/workflow_transition.py <slug> <stage>' instead.")
    print("No action taken.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
try:
    rc = subprocess.call(args)
    sys.exit(rc)
except Exception as e:
    print(f"Failed to forward to sync_status.py: {e}")
    sys.exit(2)
