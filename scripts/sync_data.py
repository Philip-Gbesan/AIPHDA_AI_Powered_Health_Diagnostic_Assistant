import os
import shutil
import sys
import subprocess  # <-- needed for running other scripts

def sync_data():
    ADMIN_UPLOADS = "uploads/admin_datasets/"
    RAW_DIR = "ml/data/raw/"

    print("=== Syncing Admin Uploaded Datasets ===")

    os.makedirs(ADMIN_UPLOADS, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)

    # Move uploaded CSVs into raw data folder
    for filename in os.listdir(ADMIN_UPLOADS):
        if filename.lower().endswith(".csv"):
            src = os.path.join(ADMIN_UPLOADS, filename)
            dest = os.path.join(RAW_DIR, filename)
            print(f"Importing dataset: {filename}")
            shutil.copy2(src, dest)

    print("✅ Datasets synced successfully.")

    # Optional: run preprocessing if --reprocess flag is passed
    if "--reprocess" in sys.argv:
        preprocess_script = os.path.join("ml", "run_preprocess.py")
        if os.path.exists(preprocess_script):
            print("Running preprocessing...")
            subprocess.run([sys.executable, preprocess_script], check=True)
            print("✅ Preprocessing complete.")
        else:
            print(f"[WARNING] Preprocess script not found at {preprocess_script}")

    print("=== Sync Complete ===")

if __name__ == "__main__":
    sync_data()
