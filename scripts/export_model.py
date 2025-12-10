import sys
import os
import shutil
import json
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.queries import register_model_version  # make sure db.py uses absolute path

MODEL_SRC = os.path.join(PROJECT_ROOT, "ml/model/rf_model.joblib")
MODEL_DEST = os.path.join(PROJECT_ROOT, "ml/model/saved_models")
META_DEST = os.path.join(MODEL_DEST, "meta.json")

def export_model():
    os.makedirs(MODEL_DEST, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_model = f"rf_model_{timestamp}.joblib"

    print("Exporting model...")

    if not os.path.exists(MODEL_SRC):
        raise FileNotFoundError(f"Model not found at: {MODEL_SRC}")

    dest_path = os.path.join(MODEL_DEST, versioned_model)
    shutil.copy2(MODEL_SRC, dest_path)

    latest_model = os.path.join(MODEL_DEST, "latest_model.joblib")
    shutil.copy2(dest_path, latest_model)

    metadata = {"version": versioned_model, "timestamp": timestamp}
    with open(META_DEST, "w") as f:
        json.dump(metadata, f, indent=4)


    # 5️⃣ Register in DB
    try:
        register_model_version(
            version=versioned_model,
            path=dest_path,
            accuracy=None,      # optional
            top3_accuracy=None  # optional
        )
    except Exception as e:
        print(f"[ERROR] Failed to register model in DB: {e}")
        raise


    print("Model exported and registered successfully")
    print(f"Version: {versioned_model}")


if __name__ == "__main__":
    export_model()
