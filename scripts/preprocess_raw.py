"""
Admin-triggered preprocessing script.
Calls the real high-level pipeline at ml/run_preprocess.py
"""

import subprocess
import sys
import os

def run_preprocessing():
    print("=== Running Preprocessing Pipeline (Admin Trigger) ===")

    # Use server's Python interpreter
    python = sys.executable

    # Project root (two levels up from this file)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Absolute path to run_preprocess.py
    script_path = os.path.join(BASE_DIR, "ml", "run_preprocess.py")

    if not os.path.exists(script_path):
        print(f"❌ ERROR: run_preprocess.py not found at: {script_path}")
        return 1

    # Run script in project root to avoid import/path issues
    result = subprocess.run(
        [python, script_path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    # Show console output to Flask log and Admin UI
    print(result.stdout)

    if result.returncode != 0:
        print("❌ Preprocessing FAILED")
        print(result.stderr)
        return result.returncode

    print("✅ Preprocessing completed successfully")
    return 0


if __name__ == "__main__":
    run_preprocessing()
