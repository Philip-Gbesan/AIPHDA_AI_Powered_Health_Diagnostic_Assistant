import os
import unittest
import subprocess
import time
import glob
import shutil

SCRIPTS_DIR = "scripts"
MODEL_DIR = "backend/model/"
RAW_DIR = "ml/data/raw/"
UPLOADS_DIR = "uploads/admin_datasets/"

def run_script(script_name, *args):
    bash = shutil.which("bash")

    if bash is None:
        raise EnvironmentError(
            "Bash shell not found. Install Git Bash or WSL to run shell scripts on Windows."
        )

    cmd = [bash, f"{SCRIPTS_DIR}/{script_name}"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)



class ScriptIntegrationTest(unittest.TestCase):

    def setUp(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        os.makedirs(RAW_DIR, exist_ok=True)
        os.makedirs(UPLOADS_DIR, exist_ok=True)

    # ------------------------------------------------------------
    # TEST 1 - export_model.sh
    # ------------------------------------------------------------
    def test_export_model(self):
        print("\nRunning export_model.sh...")

        # Run script
        result = run_script("export_model.sh")
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

        # Find exported model
        exported_models = glob.glob(os.path.join(MODEL_DIR, "rf_model_*.joblib"))
        self.assertGreater(len(exported_models), 0, "No exported model found in backend/model/")

        # Check metadata exists
        meta_path = os.path.join(MODEL_DIR, "meta.json")
        self.assertTrue(os.path.exists(meta_path), "meta.json missing")

        print("✓ export_model.sh works")

    # ------------------------------------------------------------
    # TEST 2 - retrain.sh
    # ------------------------------------------------------------
    def test_retrain_script(self):
        print("\nRunning retrain.sh...")

        # Run retraining
        result = run_script("retrain.sh")
        self.assertEqual(result.returncode, 0, f"Retrain failed: {result.stderr}")

        # Verify model retrained
        models = glob.glob("ml/model/rf_model.joblib")
        self.assertGreater(len(models), 0, "Model was not retrained")

        # Verify export step ran
        backend_models = glob.glob(os.path.join(MODEL_DIR, "rf_model_*.joblib"))
        self.assertGreater(len(backend_models), 0, "Model was not exported to backend")

        print("✓ retrain.sh works")

    # ------------------------------------------------------------
    # TEST 3 - sync_data.sh
    # ------------------------------------------------------------
    def test_sync_data_script(self):
        print("\nRunning sync_data.sh...")

        # Create a fake admin-uploaded dataset
        test_csv = os.path.join(UPLOADS_DIR, "test_dataset.csv")
        with open(test_csv, "w") as f:
            f.write("symptom,disease\nfever,flu")

        # Run script
        result = run_script("sync_data.sh")
        self.assertEqual(result.returncode, 0, f"sync_data.sh failed: {result.stderr}")

        # Check file copied to raw directory
        synced_file = os.path.join(RAW_DIR, "test_dataset.csv")
        self.assertTrue(os.path.exists(synced_file), "Dataset was not synced to raw directory")

        print("✓ sync_data.sh works")

    # Optional: test sync + reprocess flag
    def test_sync_data_with_reprocess(self):
        print("\nRunning sync_data.sh --reprocess")

        result = run_script("sync_data.sh", "--reprocess")
        self.assertEqual(result.returncode, 0, "sync_data.sh --reprocess failed")

        print("✓ sync_data.sh --reprocess runs preprocessing")


if __name__ == "__main__":
    unittest.main()



## Run this file using git bash with this command """python -m tests.test_scripts"""
## Trust me it won't work in powershell if you try it I've been there 🥲 
## You've got to run it this way with this specific command above or it probably might not run 

## And be patient this is the most time consuming test since it has to test the Preprocessing of the data 
## The Training of the model, Exporting the model and versioning it, 
## Syncing dataset uploaded by the admin and adding them to the raw dataset for 
## preprocessing before training and the whole cycle again
