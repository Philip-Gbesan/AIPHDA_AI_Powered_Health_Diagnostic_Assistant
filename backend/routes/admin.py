import os
import sys
from flask import send_file
import zipfile
import io
import subprocess
from flask import Blueprint, request, jsonify
from database.queries import (
    register_admin_dataset,
    get_admin_datasets,
    get_models,
    get_prediction_logs,
    get_symptom_trends,
    create_prediction_attempt
)

admin_bp = Blueprint("admin", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")

# ======================
# UPLOAD DATASET
# ======================
@admin_bp.route("/upload-dataset", methods=["POST"])
def upload_dataset():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "file is required"}), 400

    filename = "uploaded_" + file.filename
    save_path = f"ml/data/raw/{filename}"
    file.save(save_path)

    register_admin_dataset(filename, "pending")

    return jsonify({
        "message": "Dataset uploaded",
        "filename": filename
    })


# ======================
# LIST DATASETS
# ======================
@admin_bp.route("/datasets", methods=["GET"])
def list_datasets():
    return jsonify(get_admin_datasets())


# ======================
# LIST MODELS
# ======================
@admin_bp.route("/models", methods=["GET"])
def list_models():
    return jsonify(get_models())

def run_python_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    env = os.environ.copy()
    env["FLASK_RUN_FROM_CLI"] = "false"  # Prevent Flask reload on script changes

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        env=env
    )


    return result


# ======================
# SAVE MODEL
# ======================
@admin_bp.route("/save-model", methods=["POST"])
def save_model():
    result = run_python_script("export_model.py")

    if result.returncode != 0:
        return jsonify({
            "error": "Export script failed",
            "details": result.stderr
        }), 500

    return jsonify({
        "message": "Model saved successfully",
        "output": result.stdout
    })


# ======================
# RETRAIN MODEL
# ======================
@admin_bp.route("/retrain", methods=["POST"])
def retrain():
    result = run_python_script("retrain.py")

    if result.returncode != 0:
        return jsonify({
            "error": "Retrain script failed",
            "details": result.stderr
        }), 500

    return jsonify({
        "message": "Retraining complete",
        "output": result.stdout
    })


# ======================
# SYNC RAW DATA
# ======================
@admin_bp.route("/sync-data", methods=["POST"])
def sync_data():
    result = run_python_script("sync_data.py")

    if result.returncode != 0:
        return jsonify({
            "error": "Sync script failed",
            "details": result.stderr
        }), 500

    return jsonify({
        "message": "Datasets synced successfully",
        "output": result.stdout
    })


@admin_bp.route("/preprocess", methods=["POST"])
def preprocess():
    result = run_python_script("preprocess_raw.py")

    if result.returncode != 0:
        return jsonify({"error": "Preprocess failed", "details": result.stderr}), 500

    return jsonify({"message": "Preprocessing complete", "output": result.stdout})


@admin_bp.route("/revert-model", methods=["POST"])
def revert_model():
    result = run_python_script("revert_model.py")

    if result.returncode != 0:
        return jsonify({
            "error": "Revert failed",
            "stdout": result.stdout,
            "stderr": result.stderr
        }), 500


    return jsonify({"message": "Model reverted", "output": result.stdout})



@admin_bp.route("/download-model", methods=["GET"])
def download_model():
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, 'w') as zipf:
        zipf.write("ml/model/rf_model.joblib", arcname="rf_model.joblib")

        meta = "ml/model/meta.json"
        if os.path.exists(meta):
            zipf.write(meta, arcname="meta.json")

    buffer.seek(0)

    return send_file(buffer,
                     mimetype="application/zip",
                     as_attachment=True,
                     download_name="current_model_bundle.zip")


# ======================
# PREDICTION LOGS
# ======================
@admin_bp.route("/logs", methods=["GET"])
def logs():
    return jsonify(get_prediction_logs())


# ======================
# SYMPTOM TRENDS
# ======================
@admin_bp.route("/symptom-trends", methods=["GET"])
def symptom_trends():
    return jsonify(get_symptom_trends())


# ======================
# FRONTEND COUNTER (OPTIONAL)
# ======================
@admin_bp.route("/record-check", methods=["POST"])
def record_check():
    data = request.get_json() or {}
    symptoms = data.get("symptoms", "")
    check_id = create_prediction_attempt(symptoms)
    return jsonify({"check_id": check_id}), 201


# ======================
# SIMPLE STATS ENDPOINT
# ======================
admin_stats = {"total_checks": 0, "successful_checks": 0}

@admin_bp.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(admin_stats)
