"""
Database Test Suite for AI Health Diagnostic Assistant

This script tests:
- Database connection
- Table existence
- Insert queries
- Select queries
- Update queries
- All functions in database/queries.py

Run using:
    python -m tests.test_db
"""

import unittest
import sqlite3
from database.db import get_connection
from database.queries import (
    save_model_metadata,
    save_feedback,
    log_prediction,
    register_admin_dataset,
    get_models,
    get_feedback,
    get_prediction_logs,
    get_admin_datasets,
    increment_symptom_counts,
    get_symptom_trends
)


DB_PATH = "database/dev.sqlite"


class DatabaseTestCase(unittest.TestCase):

    # ---------------------------
    # DB CONNECTION
    # ---------------------------
    def test_connection(self):
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()
        print("\n✓ DB connection OK")

    # ---------------------------
    # TABLE CHECK
    # ---------------------------
    def test_tables_exist(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = set(t[0] for t in c.fetchall())

        required = {
            "models",
            "features",
            "user_feedback",
            "admin_uploaded_datasets",
            "prediction_logs",
            "symptom_trends"
        }

        self.assertTrue(required.issubset(tables))
        conn.close()
        print("✓ All required tables exist")

    # ---------------------------
    # MODEL METADATA
    # ---------------------------
    def test_save_and_get_models(self):
        save_model_metadata("v1-test", "model/test.joblib", 0.90, 0.95)
        models = get_models()
        self.assertGreater(len(models), 0)
        print("✓ save_model_metadata + get_models OK")

    # ---------------------------
    # FEEDBACK
    # ---------------------------
    def test_save_and_get_feedback(self):
        save_feedback("['fever']", "flu", None, "accurate")
        rows = get_feedback()
        self.assertGreater(len(rows), 0)
        print("✓ save_feedback + get_feedback OK")

    # ---------------------------
    # PREDICTION LOGS
    # ---------------------------
    def test_log_and_get_predictions(self):
        log_prediction("['fever']", "[{'cond':'flu'}]", "flu")
        logs = get_prediction_logs()
        self.assertGreater(len(logs), 0)
        print("✓ log_prediction + get_prediction_logs OK")

    # ---------------------------
    # ADMIN DATASET REGISTRATION
    # ---------------------------
    def test_register_and_get_datasets(self):
        register_admin_dataset("uploaded_test.csv", "pending")
        datasets = get_admin_datasets()
        self.assertGreater(len(datasets), 0)
        print("✓ register_admin_dataset + get_admin_datasets OK")

    # ---------------------------
    # SYMPTOM TRENDS
    # ---------------------------
    def test_symptom_trends(self):
        increment_symptom_counts(["fever", "cough"])
        rows = get_symptom_trends()
        self.assertGreater(len(rows), 0)
        print("✓ increment_symptom_counts + get_symptom_trends OK")


if __name__ == "__main__":
    unittest.main()



## Run this file using git bash with this command """python -m tests.test_db"""
## You've got to run it this way with this specific command above or it probably might not run 