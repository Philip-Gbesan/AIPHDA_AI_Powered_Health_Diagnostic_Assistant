from flask import Blueprint, request, jsonify
from database.queries import log_feedback
from backend.routes.admin import admin_stats

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("", methods=["POST"])
def receive_feedback():
    data = request.get_json() or {}

    symptoms = data.get("symptoms", [])
    predicted = data.get("predicted", "")
    feedback = data.get("feedback", "")

    if not predicted:
        return jsonify({"error": "Missing predicted condition"}), 400

    # Save feedback in database
    log_feedback(symptoms=str(symptoms), predicted=predicted, feedback=feedback)

    # If accurate → increment successful checks
    if feedback == "accurate":
        admin_stats["successful_checks"] += 1

    return jsonify({"message": "Feedback recorded"})
