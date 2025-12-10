import joblib
import json
from ml.preprocess.merger.vector_builder import VectorBuilder
from database.db import get_connection

MODEL_PATH = "ml/model/rf_model.joblib"
FEATURES_PATH = "ml/data/processed/features.json"

class MLService:
    def __init__(self):
        print("Loading model and features...")
        model_obj = joblib.load(MODEL_PATH)

        self.model = model_obj["model"]
        self.label_encoder = model_obj["label_encoder"]

        with open(FEATURES_PATH, "r") as f:
            feature_index = json.load(f)
        
        self.features = feature_index  
        self.vector_builder = VectorBuilder(feature_index)
        print("ML service ready.")

    def predict(self, symptoms_list):
        """
        symptoms_list: ["fever", "cough"]
        """
        vector = self.vector_builder.build_vector(symptoms_list).reshape(1, -1)
        proba = self.model.predict_proba(vector)[0]

        # top 3
        top3_idx = proba.argsort()[::-1][:3]
        conditions = self.label_encoder.inverse_transform(top3_idx)

        return [
            {
                "condition": cond,
                "probability": float(proba[i])
            }
            for i, cond in zip(top3_idx, conditions)
        ]

# Global Singleton
ml_service = MLService()
