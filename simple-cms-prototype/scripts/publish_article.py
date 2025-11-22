import shutil
import sys
import sys

def main():
    print("Deprecated: 'publish_article.py' has been retired. Use 'scripts/workflow_transition.py <slug> Approved' instead.")
    print("No action taken.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
    shutil.move(source_path, dest_path)
    print(f"Moved {article_file} to published folder")
else:
    print("File not found in articles folder")
