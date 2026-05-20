"""
TrendPulse — Task 4
Matplotlib charts from clean_data.csv (500 posts after Task 2 from trends.json).
"""

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Same loading as task 3: clean_data.csv from Task 2 (sourced from trends.json).
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
            hint = " Run: python task2_clean_csv.py first."
        raise SystemExit("Need clean_data.csv from Task 2." + hint)
    df = pd.read_csv(csv_files[0])
    if "comments" not in df.columns and "num_comments" in df.columns:
        df = df.rename(columns={"num_comments": "comments"})

print(f"Plotting {len(df)} posts.\n")

os.makedirs("data", exist_ok=True)

# Histogram — score distribution
plt.hist(df["score"])
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("data/task4_score_distribution.png", bbox_inches="tight")
plt.show()

# Scatter — score vs comments
plt.figure()
plt.scatter(df["score"], df["comments"])
plt.xlabel("Score")
plt.ylabel("Comments")
plt.title("Score vs Comments")
plt.tight_layout()
plt.savefig("data/task4_score_vs_comments.png", bbox_inches="tight")
plt.show()

# Bar chart — top 5 posts by score
top5 = df.sort_values(by="score", ascending=False).head()

plt.figure()
plt.barh(top5["title"], top5["score"])
plt.title("Top 5 Posts")
plt.tight_layout()
plt.savefig("data/task4_top5_posts.png", bbox_inches="tight")
plt.show()

# Box plot to know the outliers in the score column
plt.figure()
plt.boxplot(df["score"])
plt.title("Score Boxplot")
plt.show()

# Bar chart to know the average score by category
avg_scores = df.groupby("category")["score"].mean()
plt.figure()
plt.bar(avg_scores.index, avg_scores.values)
plt.title("Average Score by Category")
plt.xticks(rotation=45)
plt.show()

# Line chart to know the score trend
plt.figure()
plt.plot(df["score"].head(50))
plt.title("Score Trend")
plt.xlabel("Posts")
plt.ylabel("Score")
plt.show()

# Pie chart to know the category distribution
category_counts = df["category"].value_counts()
plt.figure()
plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
plt.title("Category Distribution")
plt.show()