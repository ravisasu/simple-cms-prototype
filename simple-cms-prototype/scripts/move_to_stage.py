import sys

def main():
    print("Deprecated: 'move_to_stage.py' has been retired. Use 'scripts/workflow_transition.py <slug> <stage>' instead (only Approved triggers publish move).")
    print("No action taken.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
