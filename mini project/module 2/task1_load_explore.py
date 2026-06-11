# Task 1 - load and explore churnguard dataset

import pandas as pd

# step 1 - load the raw csv file into a dataframe
df = pd.read_csv("churnguard_data.csv")

# step 2 - check how many rows and columns we have
print("Shape:", df.shape)

# step 3 - look at first few records
print("\nFirst 5 rows:")
print(df.head())

# step 4 - see column names and data types
print("\nColumn names and data types:")
print(df.info())

# step 5 - find missing values in each column
print("\nMissing values in each column:")
print(df.isnull().sum())

# step 6 - count duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

# step 7 - check churn column (has inconsistent yes/no entries)
print("\nChurn value counts:")
print(df["Churn"].value_counts())

# step 8 - check contract column (has typos and different spellings)
print("\nUnique values in Contract column:")
print(df["Contract"].unique())
