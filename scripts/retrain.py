"""
Full ML retraining pipeline:
1. Preprocess raw datasets
2. Train + evaluate RandomForest model
3. Export versioned model into saved_models
"""

import os
import sys
import subprocess
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON = sys.executable  # automatically uses current venv/python

def run_step(label, command):
    """Run a step and fail cleanly with readable error output."""
    print(f"\n=== {label} ===")
    try:
        subprocess.run([PYTHON] + command, check=True)
        print(f"{label} completed.")
    except subprocess.CalledProcessError:
        print(f"❌ {label} FAILED!")
        traceback.print_exc()
        sys.exit(1)

def retrain():
    print("\n====================")
    print("  ML RETRAIN START")
    print("====================\n")

    # --- Ensure scripts run from the correct directory ---
    os.chdir(PROJECT_ROOT)

    # # 1. PREPROCESS
    # run_step(
    #     "Preprocessing",
    #     ["ml/run_preprocess.py"]
    # )

    # 2. TRAIN & EVALUATE
    run_step(
        "Training + Evaluation",
        ["ml/run_train_eval.py"]
    )

    # 3. EXPORT LATEST MODEL
    run_step(
        "Exporting Versioned Model",
        ["scripts/export_model.py"]
    )

    print("\n====================")
    print(" ML RETRAIN COMPLETE")
    print("====================\n")
    return True


if __name__ == "__main__":
    success = retrain()
    sys.exit(0 if success else 1)
