# Task 2 - clean the churnguard dataset

import pandas as pd

# step 1 - load the raw csv file
df = pd.read_csv("churnguard_data.csv")

# step 2 - drop customerID (not needed for modelling)
df = df.drop(columns=["customerID"])

# step 3 - remove duplicate rows
df = df.drop_duplicates()

# step 4 - strip extra spaces from gender and payment method
df["gender"] = df["gender"].str.strip()
df["PaymentMethod"] = df["PaymentMethod"].str.strip()

# step 5 - fix inconsistent yes/no casing
df["Churn"] = df["Churn"].str.strip().str.title()
df["PhoneService"] = df["PhoneService"].str.strip().str.title()
df["PaperlessBilling"] = df["PaperlessBilling"].str.strip().str.title()

# step 6 - map contract typos to three valid values
contract_fix = {
    "month-to-month": "Month-to-month",
    "month to month": "Month-to-month",
    "monthly": "Month-to-month",
    "one year": "One year",
    "1 year": "One year",
    "two year": "Two year",
    "2 year": "Two year",
}
df["Contract"] = df["Contract"].str.strip().str.lower().map(contract_fix)

# step 7 - map internet service typos to three valid values
internet_fix = {
    "dsl": "DSL",
    "fiber optic": "Fiber optic",
    "fibre optic": "Fiber optic",
    "fiberoptic": "Fiber optic",
    "no": "No",
}
df["InternetService"] = df["InternetService"].str.strip().str.lower().map(internet_fix)

# step 8 - convert total charges to number (junk becomes NaN)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# step 9 - remove bad tenure values (zero or negative)
df = df[df["tenure"] > 0]

# step 10 - remove monthly charge outliers
df = df[(df["MonthlyCharges"] >= 10) & (df["MonthlyCharges"] <= 200)]

# step 11 - fill remaining missing values
df["MonthlyCharges"] = df["MonthlyCharges"].fillna(df["MonthlyCharges"].mean())
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].mean())
df["tenure"] = df["tenure"].fillna(df["tenure"].median()).round().astype(int)

# step 12 - print shape after cleaning
print("Shape after cleaning:", df.shape)

# step 13 - check no missing values left
print("\nMissing values after cleaning:")
print(df.isnull().sum())
