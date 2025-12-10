"""
Unit + Integration Test for AI Health Diagnostic Assistant ML Pipeline.
Runs checks on:
- Model loading
- Vectorization process
- Basic prediction correctness
- Top-1 and Top-3 evaluation accuracy

Run:
    python test_ml.py
"""

import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Import components from your ML pipeline
from ml.preprocess.merger.feature_indexer import FeatureIndexer
from ml.preprocess.merger.vector_builder import VectorBuilder


MASTER = "ml/data/processed/master_dataset.csv"
FEATURES = "ml/data/processed/features.json"
MODEL = "ml/model/rf_model.joblib"


# ---------------------
# Utility evaluation
# ---------------------
def top_k_accuracy(clf, X, y_true, k=3):
    proba = clf.predict_proba(X)
    topk = np.argsort(proba, axis=1)[:, ::-1][:, :k]
    correct = 0
    for i, row in enumerate(topk):
        if y_true[i] in row:
            correct += 1
    return correct / len(y_true)


# ---------------------
# Main test routine
# ---------------------
def test_ml_system():
    print("\n=== Running ML System Test ===\n")

    # 1. Check required files exist
    for f in [MASTER, FEATURES, MODEL]:
        if not Path(f).exists():
            raise FileNotFoundError(f"\n❌ Required file not found: {f}\nRun preprocessing + training first.")

    print("✓ Required files exist")

    # 2. Load master dataset
    df = pd.read_csv(MASTER)
    if df.empty:
        raise ValueError("❌ Master dataset is empty!")

    print(f"✓ Loaded master dataset ({len(df)} records)")

    # 3. Load feature index
    features = FeatureIndexer.load(FEATURES)
    vb = VectorBuilder(features)
    print(f"✓ Loaded {len(features)} symptoms into feature index")

    # 4. Convert dataset to vectors
    X, y = vb.dataset_to_matrix(df)
    if X.size == 0:
        raise ValueError("❌ Vectorized dataset is empty!")

    print("✓ Converted dataset into binary vectors")

    # 5. Load trained model
    model_obj = joblib.load(MODEL)
    clf = model_obj["model"]
    le = model_obj["label_encoder"]

    print("✓ Loaded RandomForest model & LabelEncoder")

    # 6. Encode labels
    y_enc = le.transform(y)
    print("✓ Converted labels to encoded form")

    # 7. Evaluate accuracy
    from sklearn.metrics import accuracy_score

    top1 = accuracy_score(y_enc, clf.predict(X))
    top3 = top_k_accuracy(clf, X, y_enc, k=3)

    print("\n=== Evaluation Results ===")
    print(f"Top-1 Accuracy: {top1:.4f}")
    print(f"Top-3 Accuracy: {top3:.4f}")

    # 8. Random sample test
    print("\n=== Sample Predictions ===")
    sample_rows = min(5, len(df))
    sample = df.sample(sample_rows)

    for idx, row in sample.iterrows():
        symptoms = row["symptoms"]
        # Convert symptom list to vector
        vec = vb.build_vector(eval(symptoms) if isinstance(symptoms, str) and symptoms.startswith("[") else symptoms)
        vec = vec.reshape(1, -1)
        proba = clf.predict_proba(vec)[0]
        top3_indices = np.argsort(proba)[::-1][:3]
        top3_labels = le.inverse_transform(top3_indices)

        print(f"\nInput Symptoms: {symptoms}")
        print("Top Predictions:")
        for i, label in enumerate(top3_labels):
            print(f"  {i+1}. {label} (prob={proba[top3_indices[i]]:.4f})")

    print("\n✓ ML Pipeline Test Completed Successfully!")



if __name__ == "__main__":
    test_ml_system()


## Run this file using git bash with this command """python -m tests.test_ml"""
## You've got to run it this way with this specific command above or it probably might not run 