import os
import shutil
import glob

MODEL_DIR = "ml/model/"
SAVED_DIR = "ml/model/saved_models/"

def revert():
    saved = sorted(
        glob.glob(os.path.join(SAVED_DIR, "*.joblib")),
        key=os.path.getmtime
    )

    if len(saved) < 2:
        print("Not enough model versions to revert.")
        exit(1)

    last_model = saved[-2]   # previous version
    dest = os.path.join(MODEL_DIR, "rf_model.joblib")

    shutil.copy(last_model, dest)
    print("Reverted to:", last_model)

if __name__ == "__main__":
    revert()
