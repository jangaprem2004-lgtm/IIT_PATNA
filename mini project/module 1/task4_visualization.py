# Task 4 - plots from clean_data.csv

import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("clean_data.csv")
print("plotting", len(df), "posts")

os.makedirs("data", exist_ok=True)

# histogram of scores
plt.hist(df["score"])
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.savefig("data/task4_score_distribution.png")
plt.show()

# scatter score vs comments
plt.figure()
plt.scatter(df["score"], df["comments"])
plt.xlabel("Score")
plt.ylabel("Comments")
plt.title("Score vs Comments")
plt.savefig("data/task4_score_vs_comments.png")
plt.show()

# top 5 posts by score
top5 = df.sort_values(by="score", ascending=False).head()
plt.figure()
plt.barh(top5["title"], top5["score"])
plt.title("Top 5 Posts")
plt.savefig("data/task4_top5_posts.png")
plt.show()

# boxplot for outliers
plt.figure()
plt.boxplot(df["score"])
plt.title("Score Boxplot")
plt.show()

# average score by category
avg_scores = df.groupby("category")["score"].mean()
plt.figure()
plt.bar(avg_scores.index, avg_scores.values)
plt.title("Average Score by Category")
plt.xticks(rotation=45)
plt.show()

# score trend for first 50 posts
plt.figure()
plt.plot(df["score"].head(50))
plt.title("Score Trend")
plt.xlabel("Posts")
plt.ylabel("Score")
plt.show()

# category pie chart
category_counts = df["category"].value_counts()
plt.figure()
plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
plt.title("Category Distribution")
plt.show()

print("visualization successful")
