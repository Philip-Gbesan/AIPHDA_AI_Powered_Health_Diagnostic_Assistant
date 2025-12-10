"""
High-level preprocessing entrypoint.
Runs: auto-loading → cleaning → merging → feature mapping → master dataset creation.
"""

import json
from pathlib import Path
from preprocess.pipeline import main as run_pipeline

RAW_DIR = "ml/data/raw"
OUT_DIR = "ml/data/processed"
SYNONYMS = "ml/preprocess/cleaners/synonyms_map.json"

if __name__ == "__main__":
    print("\n=== AI Health Assistant — PREPROCESSING PIPELINE ===")
    print("Scanning raw datasets at:", RAW_DIR)
    
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    run_pipeline(
        raw_dir=RAW_DIR,
        out_dir=OUT_DIR,
        synonyms_path=SYNONYMS
    )

    print("\nPreprocessing complete.")
    print("Master dataset saved at:", f"{OUT_DIR}/master_dataset.csv")
    print("Feature index saved at:", f"{OUT_DIR}/features.json")
