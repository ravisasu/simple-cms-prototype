import json
import sys
from datetime import datetime

article_id = sys.argv[1]
new_status = sys.argv[2]

with open("content_status.json", "r") as f:
    data = json.load(f)

found = False

for article in data["articles"]:
    if article["id"] == article_id:
        article["current_status"] = new_status
        article["last_updated"] = str(datetime.now().date())
        found = True
        break

if not found:
    print("Article ID not found in content_status.json")
else:
    with open("content_status.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated {article_id} → {new_status}")
