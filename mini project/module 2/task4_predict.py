# Task 4 - predict churn for a single customer

import pandas as pd
from sklearn.linear_model import LogisticRegression

# step 1 - load data and apply task 2 cleaning steps
df = pd.read_csv("churnguard_data.csv")

df = df.drop(columns=["customerID"])
df = df.drop_duplicates()

df["gender"] = df["gender"].str.strip()
df["PaymentMethod"] = df["PaymentMethod"].str.strip()

df["Churn"] = df["Churn"].str.strip().str.title()
df["PhoneService"] = df["PhoneService"].str.strip().str.title()
df["PaperlessBilling"] = df["PaperlessBilling"].str.strip().str.title()

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

internet_fix = {
    "dsl": "DSL",
    "fiber optic": "Fiber optic",
    "fibre optic": "Fiber optic",
    "fiberoptic": "Fiber optic",
    "no": "No",
}
df["InternetService"] = df["InternetService"].str.strip().str.lower().map(internet_fix)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df[df["tenure"] > 0]
df = df[(df["MonthlyCharges"] >= 10) & (df["MonthlyCharges"] <= 200)]

df["MonthlyCharges"] = df["MonthlyCharges"].fillna(df["MonthlyCharges"].mean())
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].mean())
df["tenure"] = df["tenure"].fillna(df["tenure"].median()).round().astype(int)

# step 2 - encode target column (yes=1, no=0)
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# encode contract as number (0=month-to-month, 1=one year, 2=two year)
df["Contract"] = df["Contract"].map({"Month-to-month": 0, "One year": 1, "Two year": 2})

# use only 5 features for training
feature_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Contract"]
X = df[feature_cols]
y = df["Churn"]

# step 3 - train model on full cleaned dataset
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# step 4 - take customer details from user
tenure = int(input("Enter tenure (months): "))
monthly_charges = float(input("Enter Monthly Charges: "))
total_charges = float(input("Enter Total Charges: "))
senior_citizen = int(input("Senior Citizen? (1 = Yes, 0 = No): "))
contract = int(input("Contract type (0 = Month-to-month, 1 = One year, 2 = Two year): "))

# step 5 - make prediction
customer = pd.DataFrame(
    [[tenure, monthly_charges, total_charges, senior_citizen, contract]],
    columns=feature_cols,
)
prediction = model.predict(customer)[0]

# step 6 - print result
if prediction == 1:
    print("Prediction: This customer is likely to CHURN.")
else:
    print("Prediction: This customer is likely to STAY.")
