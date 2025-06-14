import joblib
import numpy as np

class EligibilityAgent:
    def __init__(self, model_path="models/eligibility_model.pkl"):
        self.model = joblib.load(model_path)

    def prepare_features(self, extracted_data):
        income = extracted_data.get('estimated_income') or extracted_data.get('credit_income') or 0
        family_size = extracted_data.get('family_size', 3)
        asset_list = extracted_data.get('assets_info', [])
        asset_value = sum([a.get('Value', 0) for a in asset_list])
        employment_status = 1 if "employed" in extracted_data.get('resume_text', "").lower() else 0
        resume_len = len(extracted_data.get('resume_text', ""))

        return np.array([[income, family_size, asset_value, employment_status, resume_len]])

    def predict(self, extracted_data):
        features = self.prepare_features(extracted_data)
        pred = self.model.predict(features)[0]
        prob = self.model.predict_proba(features)[0][1]
        return {
            "eligible": bool(pred),
            "confidence": round(prob, 2)
        }