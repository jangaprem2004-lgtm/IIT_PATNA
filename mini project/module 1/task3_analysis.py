# Task 3 - EDA on clean_data.csv

import pandas as pd
import numpy as np

df = pd.read_csv("clean_data.csv")
print("loaded", len(df), "posts")
print(df.info())
print(df.head())

print("Average Score:", np.mean(df["score"]))
print("Max Score:", np.max(df["score"]))
print("Min Score:", np.min(df["score"]))

print("\nMost commented post:")
print(df.loc[df["comments"].idxmax()])

print("\nHighest score post:")
print(df.loc[df["score"].idxmax()])

print("\nTop 5 posts by score:")
print(df.sort_values(by="score", ascending=False).head())

print("\nScore distribution:")
print(df["score"].describe())

print("\nBefore dropping duplicates:", len(df))
df = df.drop_duplicates(subset="title")
print("After dropping duplicates:", len(df))

# remove high score outliers
df = df[df["score"] < 1000]
print("After removing score outliers:", len(df))

print("\nComments column stats:")
print(df["comments"].describe())

# remove high comment outliers
df = df[df["comments"] < 1000]
print("After removing comment outliers:", len(df))

print("\nAverage score by category:")
print(df.groupby("category")["score"].mean())

print("eda successful")
