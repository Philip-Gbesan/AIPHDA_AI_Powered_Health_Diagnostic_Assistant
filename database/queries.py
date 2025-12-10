from .db import get_connection
import json

# ====================================
# MODEL METADATA
# ====================================

def save_model_metadata(version, path, acc, top3):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO models (version, path, accuracy, top3_accuracy)
            VALUES (?, ?, ?, ?)
        """, (version, path, acc, top3))
        conn.commit()
    finally:
        conn.close()


def get_models():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT id, version, path, accuracy, top3_accuracy, created_at
            FROM models ORDER BY id DESC
        """)
        rows = c.fetchall()
    finally:
        conn.close()
    return rows


# ====================================
# MODEL MANAGEMENT
# ====================================

def register_model_version(version, path, accuracy=None, top3_accuracy=None):
    """
    Register a saved model in the database.
    """
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO models (version, path, accuracy, top3_accuracy)
            VALUES (?, ?, ?, ?)
        """, (version, path, accuracy, top3_accuracy))
        conn.commit()
    finally:
        conn.close()



# ====================================
# FEEDBACK
# ====================================

def save_feedback(symptoms, predicted, correct, feedback):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO user_feedback (user_symptoms, predicted_condition, correct_condition, feedback)
            VALUES (?, ?, ?, ?)
        """, (symptoms, predicted, correct, feedback))
        conn.commit()
    finally:
        conn.close()


def get_feedback(limit=100):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT user_symptoms, predicted_condition, correct_condition, feedback, created_at
            FROM user_feedback
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
    finally:
        conn.close()
    return rows


# ====================================
# PREDICTION LOGS
# ====================================

def log_prediction(symptoms, predictions, top_pred):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO prediction_logs (symptoms, predictions, top_prediction)
            VALUES (?, ?, ?)
        """, (symptoms, predictions, top_pred))
        conn.commit()
    finally:
        conn.close()


def get_prediction_logs(limit=50):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT symptoms, predictions, top_prediction, created_at
            FROM prediction_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
    finally:
        conn.close()
    return rows


# ====================================
# ADMIN DATASETS
# ====================================

def register_admin_dataset(filename, status="pending"):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO admin_uploaded_datasets (filename, status)
            VALUES (?, ?)
        """, (filename, status))
        conn.commit()
    finally:
        conn.close()


def get_admin_datasets():
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT id, filename, status, uploaded_at
            FROM admin_uploaded_datasets
            ORDER BY id DESC
        """)
        rows = c.fetchall()
    finally:
        conn.close()
    return rows


# ====================================
# SYMPTOM TRENDS (analytics)
# ====================================

def increment_symptom_counts(symptoms_list):
    conn = get_connection()
    try:
        c = conn.cursor()

        for symptom in symptoms_list:
            c.execute("""
                UPDATE symptom_trends
                SET count = count + 1
                WHERE symptom = ?
            """, (symptom,))

        conn.commit()
    finally:
        conn.close()


def get_symptom_trends(limit=20):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT symptom, count
            FROM symptom_trends
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
    finally:
        conn.close()
    return rows



def create_prediction_attempt(symptoms):
    """
    Insert a placeholder row into prediction_logs to represent an attempt.
    Returns the inserted row id (check_id).
    """
    conn = get_connection()
    try: 
        c = conn.cursor()
        c.execute("""
            INSERT INTO prediction_logs (symptoms, predictions, top_prediction)
            VALUES (?, ?, ?)
        """, (str(symptoms), '[]', ''))  # use empty predictions/top_prediction as placeholder
        conn.commit()
        inserted_id = c.lastrowid
    finally:
        conn.close()
    return inserted_id

def update_prediction_result(check_id, predictions, top_pred):
    """
    Update the prediction_logs row created earlier with actual predictions.
    predictions: Python list/dict -> we will store as JSON string
    """
    conn = get_connection()
    try:
        c = conn.cursor()
        preds_json = json.dumps(predictions)
        c.execute("""
            UPDATE prediction_logs
            SET predictions = ?, top_prediction = ?
            WHERE id = ?
        """, (preds_json, top_pred, check_id))
        conn.commit()
    finally:
        conn.close()