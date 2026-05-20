"""
TrendPulse — Task 2
Read raw story JSON (default: trends.json with your 500 records), tidy with pandas, save CSV.
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Full keyword set from the project handout (case matching is done on lowercased titles).
# If a title matches more than one bucket, the first category below wins.
CATEGORY_KEYWORDS = [
    (
        "technology",
        [
            "ai",
            "software",
            "tech",
            "code",
            "computer",
            "data",
            "cloud",
            "api",
            "gpu",
            "llm",
        ],
    ),
    (
        "worldnews",
        [
            "war",
            "government",
            "country",
            "president",
            "election",
            "climate",
            "attack",
            "global",
        ],
    ),
    (
        "sports",
        [
            "nfl",
            "nba",
            "fifa",
            "sport",
            "game",
            "team",
            "player",
            "league",
            "championship",
        ],
    ),
    (
        "science",
        [
            "research",
            "study",
            "space",
            "physics",
            "biology",
            "discovery",
            "nasa",
            "genome",
        ],
    ),
    (
        "entertainment",
        [
            "movie",
            "film",
            "music",
            "netflix",
            "game",
            "book",
            "show",
            "award",
            "streaming",
        ],
    ),
]


def pick_category(title: str) -> str:
    """First keyword hit wins; nothing matched -> other."""
    if not title or not isinstance(title, str):
        return "other"

    lowered = title.lower()

    for label, words in CATEGORY_KEYWORDS:
        for w in words:
            if w in lowered:
                return label

    return "other"


def newest_raw_json(data_dir: Path) -> Path:
    """Grab the latest trends_*.json so you do not have to type the path every run."""
    candidates = sorted(
        data_dir.glob("trends_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise SystemExit(f"No trends_*.json found in {data_dir}. Run task 1 first.")
    return candidates[0]


def resolve_raw_json(data_dir: Path) -> Path:
    """
    Default input for cleaning:
    1) trends.json next to this script (your 500-record file)
    2) data/trends.json
    3) newest data/trends_YYYYMMDD.json from Task 1
    """
    for candidate in (Path("trends.json"), data_dir / "trends.json"):
        if candidate.is_file():
            return candidate
    return newest_raw_json(data_dir)


def load_stories(path: Path):
    with open(path, encoding="utf-8") as fh:
        blob = json.load(fh)

    if not isinstance(blob, list):
        raise SystemExit("JSON root should be a list of story objects.")

    rows = []
    collected_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for item in blob:
        if not isinstance(item, dict):
            continue
        # HN mixes jobs, polls, etc. Stories are what we care about.
        if item.get("type") != "story":
            continue

        title = item.get("title")
        if title is None or not str(title).strip():
            continue

        rows.append(
            {
                "post_id": item.get("id"),
                "title": str(title).strip(),
                "category": pick_category(str(title)),
                "score": item.get("score"),
                "num_comments": item.get("descendants"),
                "author": item.get("by"),
                "collected_at": collected_at,
            }
        )

    return rows


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Basic housekeeping before saving."""
    if df.empty:
        return df

    # Drop dup ids if the scrape ever doubled up.
    df = df.drop_duplicates(subset=["post_id"], keep="first")

    # Make vote / comment columns numeric; NaN becomes 0 for comments.
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = (
        pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)
    )

    # Tidy text fields a bit.
    df["title"] = df["title"].str.replace(r"\s+", " ", regex=True).str.strip()
    df["author"] = df["author"].fillna("unknown").astype(str)

    return df


def main():
    parser = argparse.ArgumentParser(description="Clean TrendPulse JSON to CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to raw JSON (default: trends.json, else data/trends.json, else newest data/trends_*.json)",
    )
    args = parser.parse_args()

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    src = args.input if args.input else resolve_raw_json(data_dir)
    print(f"Reading {src}")

    rows = load_stories(src)
    df = pd.DataFrame(rows)
    df = clean_frame(df)

    # Name the csv after the date in the source filename if it matches trends_YYYYMMDD.json
    m = re.search(r"trends_(\d{8})\.json$", src.name)
    day_part = m.group(1) if m else datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = data_dir / f"trends_{day_part}.csv"

    df.to_csv(out_path, index=False)
    # Fixed filename + friendlier column name for task 3 examples (comments vs num_comments).
    df.rename(columns={"num_comments": "comments"}).to_csv("clean_data.csv", index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    print("Also saved clean_data.csv (uses column name 'comments')")


if __name__ == "__main__":
    main()
