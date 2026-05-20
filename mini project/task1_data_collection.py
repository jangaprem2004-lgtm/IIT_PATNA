"""
TrendPulse — Task 1
Pull top story IDs from Hacker News, then grab each story as JSON.
"""

import argparse
import json
import os
import time
from datetime import datetime, timezone

import requests

# HN hosts their public API on Firebase; no key needed.
BASE_URL = "https://hacker-news.firebaseio.com/v0"

# They ask for this header on every call.
HEADERS = {"User-Agent": "TrendPulse/1.0"}


def get_json(url):
    """
    GET url and parse JSON. If anything goes wrong we log it and
    return None so the rest of the script can keep going.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=25)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as err:
        print(f"Error fetching {url}: {err}")
        return None


def load_top_story_ids(limit=None):
    """
    Step 1: topstories.json is a big array of ints (newest first).
    By default we keep every id the API returns. Pass limit (e.g. 500) if you
    need to match a cap from the brief or to test on a smaller batch.
    """
    url = f"{BASE_URL}/topstories.json"
    raw = get_json(url)
    if raw is None:
        return []

    if not isinstance(raw, list):
        print("Unexpected response from topstories (not a list).")
        return []

    if limit is None:
        return raw
    return raw[:limit]


def fetch_story(story_id):
    """
    Step 2: each item lives at item/<id>.json.
    Sometimes an id is gone or not a story — the API returns null then.
    """
    url = f"{BASE_URL}/item/{story_id}.json"
    payload = get_json(url)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        print(f"Skipping id {story_id}: response was not an object.")
        return None
    return payload


def main():
    parser = argparse.ArgumentParser(description="Fetch HN top stories as JSON.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Fetch at most the first N ids (default: no cap, use full topstories list)",
    )
    args = parser.parse_args()

    print("Fetching top story id list…", flush=True)
    ids = load_top_story_ids(args.limit)
    if not ids:
        print("No ids to work with, stopping here.")
        return

    print(f"Got {len(ids)} ids. Pausing 2 seconds (rate limit from the brief)…", flush=True)

    # Brief says sleep once per category loop, not between every item.
    # Here we only have one batch (top stories), so a single pause is enough.
    time.sleep(2)

    print("Downloading each story (this can take a few minutes)…", flush=True)
    collected = []
    for n, sid in enumerate(ids, start=1):
        story = fetch_story(sid)
        if story is not None:
            collected.append(story)
        # One line every 50 requests so it does not look frozen in the terminal.
        if n % 50 == 0 or n == len(ids):
            print(f"  progress: {n}/{len(ids)} requests, {len(collected)} stories saved so far", flush=True)

    # Task 2 expects a file under data/; keep the date in the name like the brief.
    os.makedirs("data", exist_ok=True)
    day_stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    json_path = os.path.join("data", f"trends_{day_stamp}.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(collected, fh, ensure_ascii=False)

    print(f"Done. Got {len(collected)} story payloads from {len(ids)} ids.")
    print(f"Raw JSON saved to {json_path}")


if __name__ == "__main__":
    main()
