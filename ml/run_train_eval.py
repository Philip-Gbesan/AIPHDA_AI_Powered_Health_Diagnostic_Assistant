"""
High-level training + evaluation entrypoint.
Loads processed dataset → trains RandomForest → evaluates top-1 and top-3 accuracy.
"""

import os
from train import train
from evaluate import evaluate

MASTER = "ml/data/processed/master_dataset.csv"
FEATURES = "ml/data/processed/features.json"
MODEL = "ml/model/rf_model.joblib"

if __name__ == "__main__":
    print("\n=== AI Health Assistant — TRAINING & EVALUATION ===")

    if not os.path.exists(MASTER):
        print("\n❌ ERROR: No processed dataset found!")
        print("Run: python ml/run_preprocess.py first.")
        exit()

    print("\nTraining model...")
    train(
        master_csv=MASTER,
        features_json=FEATURES,
        out_model=MODEL
    )

    print("\nEvaluating model...")
    evaluate(
        master_csv=MASTER,
        features_json=FEATURES,
        model_path=MODEL
    )

    print("\nTraining + Evaluation complete!")
    print("Model saved:", MODEL)
    print("Metadata:", MODEL + ".meta.json")
    print("Evaluation:", MODEL + ".eval.json")
