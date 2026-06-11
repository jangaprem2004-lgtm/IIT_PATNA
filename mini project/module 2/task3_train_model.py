# Task 3 - train logistic regression model for churn prediction

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

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

# step 3 - one hot encode categorical columns
cat_cols = [
    "gender",
    "PhoneService",
    "InternetService",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# step 4 - separate features and target
X = df.drop(columns=["Churn"])
y = df["Churn"]

# step 5 - split into train and test (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# step 6 - train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# step 7 - predict and print accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# step 8 - print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Stay", "Churn"]))
