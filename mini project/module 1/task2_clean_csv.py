# Task 2 - read raw json and save clean csv

import json
import os
import pandas as pd
from datetime import datetime

# change this path if your json file has a different name
json_path = "data/trends.json"
if not os.path.isfile(json_path):
    json_path = "trends.json"

with open(json_path, encoding="utf-8") as f:
    raw = json.load(f)

rows = []
for item in raw:
    if item.get("type") != "story":
        continue
    title = item.get("title")
    if title is None or str(title).strip() == "":
        continue

    # simple keyword check for category
    t = str(title).lower()
    if "ai" in t or "software" in t or "tech" in t or "code" in t:
        cat = "technology"
    elif "war" in t or "government" in t or "election" in t:
        cat = "worldnews"
    elif "nba" in t or "nfl" in t or "sport" in t or "game" in t:
        cat = "sports"
    elif "research" in t or "study" in t or "space" in t or "nasa" in t:
        cat = "science"
    elif "movie" in t or "music" in t or "netflix" in t or "film" in t:
        cat = "entertainment"
    else:
        cat = "other"

    rows.append(
        {
            "post_id": item.get("id"),
            "title": str(title).strip(),
            "category": cat,
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "author": item.get("by", "unknown"),
            "collected_at": datetime.now().isoformat(),
        }
    )

df = pd.DataFrame(rows)
df = df.drop_duplicates(subset=["post_id"])
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["comments"] = pd.to_numeric(df["comments"], errors="coerce").fillna(0).astype(int)

print(df.head())
print("cleaning successful")

os.makedirs("data", exist_ok=True)
df.to_csv("clean_data.csv", index=False)
df.to_csv("data/trends_clean.csv", index=False)
print("saved", len(df), "rows to clean_data.csv")
