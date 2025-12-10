from flask import Blueprint, request, jsonify
from backend.services.ml_service import ml_service
from database.queries import update_prediction_result, log_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    symptoms = data.get("symptoms", [])
    check_id = data.get("check_id")

    try:
        # Run prediction with the real model
        predictions = ml_service.predict(symptoms)

        # Format predictions for frontend (convert 0.85 → 85)
        formatted = [
            {
                "condition": p["condition"],
                "confidence": round(p["probability"] * 100, 2)
            }
            for p in predictions
        ]

        # Log prediction (if check-id available)
        if check_id:
            top_pred = formatted[0]["condition"]
            update_prediction_result(check_id, formatted, top_pred)
        else:
            # fallback
            log_prediction(str(symptoms), str(formatted), formatted[0]["condition"])

        return jsonify({
            "predictions": formatted,
            "success": True
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
