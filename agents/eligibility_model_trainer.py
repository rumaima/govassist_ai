import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Sample data generation (replace this with your real data later)
np.random.seed(42)
n_samples = 200

data = {
    "income": np.random.randint(2000, 20000, size=n_samples),
    "family_size": np.random.randint(1, 7, size=n_samples),
    "asset_value": np.random.randint(0, 500000, size=n_samples),
    "employment_status": np.random.randint(0, 2, size=n_samples),  # 1 = employed
    "resume_len": np.random.randint(50, 5000, size=n_samples),
}

# Simple rule: if income high, resume decent, and employed => likely eligible
data["eligible"] = (
    (data["income"] > 8000) &
    (data["asset_value"] > 100000) &
    (data["employment_status"] == 1) &
    (data["resume_len"] > 200)
).astype(int)

df = pd.DataFrame(data)

# Train model
X = df[["income", "family_size", "asset_value", "employment_status", "resume_len"]]
y = df["eligible"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/eligibility_model.pkl")

print("✅ Model trained and saved at 'models/eligibility_model.pkl'")
