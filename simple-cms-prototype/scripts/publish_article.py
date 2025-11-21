import shutil
import sys
import os

article_file = sys.argv[1]

source_path = f"content/articles/{article_file}"
dest_path = f"content/published/{article_file}"

if os.path.exists(source_path):
    shutil.move(source_path, dest_path)
    print(f"Moved {article_file} to published folder")
else:
    print("File not found in articles folder")
