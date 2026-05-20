"""
TrendPulse — Task 3
NumPy + Pandas analysis on the cleaned CSV (from Task 2, built from trends.json / 500 posts).
"""

import os
from pathlib import Path

import pandas as pd
import numpy as np


# Pandas defaults right-align numbers in tables; this keeps headers/cells left-friendly.
pd.set_option("display.colheader_justify", "left")
pd.set_option("display.width", 200)


def print_row_left(row):
    """Print one story as plain lines so nothing is pushed to the right side."""
    for col in row.index:
        print(f"{col}: {row[col]}")


def print_df_left(frame):
    """Print a small dataframe flush left (no wide right-aligned number columns)."""
    # justify='left' aligns cell text to the left in the text table
    print(frame.to_string(justify="left"))

# Task 2 writes clean_data.csv from trends.json; fall back to dated CSV in data/.
if os.path.isfile("clean_data.csv"):
    df = pd.read_csv("clean_data.csv")
else:
    data_dir = Path("data")
    csv_files = sorted(
        data_dir.glob("trends_*.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not csv_files:
        hint = ""
        if Path("trends.json").is_file() or (Path("data") / "trends.json").is_file():
            hint = " Put your JSON in trends.json, then run: python task2_clean_csv.py"
        raise SystemExit(
            "Need clean_data.csv (run task2_clean_csv.py after trends.json)." + hint
        )
    df = pd.read_csv(csv_files[0])
    if "comments" not in df.columns and "num_comments" in df.columns:
        df = df.rename(columns={"num_comments": "comments"})

print(f"Analysing {len(df)} posts from cleaned data.\n")

#Information about the dataframe
print(df.info())
pd.set_option('display.max_columns', None)
print(df)

print("Average Score:", np.mean(df["score"]))
print("Max Score:", np.max(df["score"]))
print("Min Score:", np.min(df["score"]))

print("\nMost commented post:")
print_row_left(df.loc[df["comments"].idxmax()])

print("\nHighest score post:")
print_row_left(df.loc[df["score"].idxmax()])

print("\nTop 5 posts by score:")
print_df_left(df.sort_values(by="score", ascending=False).head())

# Quick view of how scores spread out (distribution).
print("\nScore distribution:")
for label, val in df["score"].describe().items():
    print(f"{label}: {val}")

#Dropping the duplicates by title
print(df.head(10),"\nBefore dropping duplicates")
df = df.drop_duplicates(subset="title")
print(df.head(10),"\nAfter dropping duplicates")

#remove outliers based on score
x = df[df["score"] < 1000]
print(x)

#info about comments column
print(df["comments"].describe())

#remove outliers based on comments
y = df[df["comments"] < 1000]
print(y)