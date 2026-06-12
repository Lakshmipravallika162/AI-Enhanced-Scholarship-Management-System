"""
ML Module: Scholarship Eligibility Prediction
Algorithm: Logistic Regression
Task: Predict Eligible / Not Eligible + Probability Score
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
import joblib
import os

# ─────────────────────────────────────────────
# 1. GENERATE / LOAD DATASET
# ─────────────────────────────────────────────
np.random.seed(42)
n = 500

data = {
    "gpa":                    np.round(np.random.uniform(2.0, 4.0, n), 2),
    "attendance_pct":         np.random.randint(50, 100, n),
    "family_income_level":    np.random.choice(["Low", "Medium", "High"], n, p=[0.4, 0.4, 0.2]),
    "previous_scholarship":   np.random.choice([0, 1], n, p=[0.6, 0.4]),
    "extracurricular_score":  np.random.randint(0, 10, n),
    "category_eligible":      np.random.choice([0, 1], n, p=[0.5, 0.5]),
}

df = pd.DataFrame(data)

# Rule-based label generation (realistic)
score = (
    (df["gpa"] >= 3.0).astype(int) * 2 +
    (df["attendance_pct"] >= 75).astype(int) * 1 +
    (df["family_income_level"] == "Low").astype(int) * 2 +
    df["previous_scholarship"] * 1 +
    (df["extracurricular_score"] >= 5).astype(int) * 1 +
    df["category_eligible"] * 1
)
df["eligible"] = (score >= 5).astype(int)

# Save dataset
os.makedirs("dataset", exist_ok=True)
df.to_csv("dataset/scholarship_dataset.csv", index=False)
print(f"Dataset saved: {df.shape[0]} rows")
print(df["eligible"].value_counts())

# ─────────────────────────────────────────────
# 2. PREPROCESSING
# ─────────────────────────────────────────────
le = LabelEncoder()
df["family_income_encoded"] = le.fit_transform(df["family_income_level"])  # High=0, Low=1, Medium=2

features = ["gpa", "attendance_pct", "family_income_encoded",
            "previous_scholarship", "extracurricular_score", "category_eligible"]
X = df[features]
y = df["eligible"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ─────────────────────────────────────────────
# 3. TRAIN LOGISTIC REGRESSION
# ─────────────────────────────────────────────
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

# ─────────────────────────────────────────────
# 4. EVALUATE
# ─────────────────────────────────────────────
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n========== MODEL EVALUATION ==========")
print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision : {precision_score(y_test, y_pred):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Not Eligible", "Eligible"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ─────────────────────────────────────────────
# 5. SAVE MODEL & ARTIFACTS
# ─────────────────────────────────────────────
os.makedirs("saved_model", exist_ok=True)
joblib.dump(model,  "saved_model/logistic_model.pkl")
joblib.dump(scaler, "saved_model/scaler.pkl")
joblib.dump(le,     "saved_model/label_encoder.pkl")
joblib.dump(features, "saved_model/feature_names.pkl")

print("\n✅ Model, scaler, and encoder saved to saved_model/")
