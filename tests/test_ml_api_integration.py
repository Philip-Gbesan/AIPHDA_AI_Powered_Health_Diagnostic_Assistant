"""
Full ML + API Integration Test
Ensures:
- ML model loads correctly inside backend
- /api/predict performs real ML inference
- Prediction is logged into the database
- Database entries match API output
"""

import unittest
import sqlite3
from backend.app import create_app
from database.db import get_connection


DB_PATH = "database/dev.sqlite"


class MLApiIntegrationTest(unittest.TestCase):

    def setUp(self):
        """Start Flask test client + reset DB logs"""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Clear prediction_logs before test
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM prediction_logs;")
        conn.commit()
        conn.close()

    # --------------------------------------------------
    # TEST ML + API END-TO-END PREDICTION
    # --------------------------------------------------
    def test_ml_api_prediction_flow(self):
        # 1. Call prediction API
        response = self.client.post(
            "/api/predict",
            json={"symptoms": ["fever", "cough"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Validate ML output
        self.assertIn("predictions", data)
        self.assertGreater(len(data["predictions"]), 0)

        top_pred = data["predictions"][0]["condition"]
        print(f"\n✓ ML model predicted: {top_pred}")

        # 2. Check if prediction was logged in DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM prediction_logs;")
        logs = c.fetchall()
        conn.close()

        self.assertGreater(len(logs), 0, "Prediction was NOT logged in DB")

        print("✓ Prediction successfully logged in DB")

        # 3. Check if logged prediction matches API output
        record = logs[0]
        logged_top_pred = record[3]  # column: top_prediction

        self.assertEqual(
            logged_top_pred,
            top_pred,
            "Logged top prediction does not match API prediction"
        )

        print("✓ Logged prediction matches API result")

    # --------------------------------------------------
    # TEST MODEL LOAD DOES NOT FAIL
    # --------------------------------------------------
    def test_model_loads_in_backend(self):
        """Ensures MLService is loaded without errors"""
        from backend.services.ml_service import ml_service

        self.assertIsNotNone(ml_service.model)
        self.assertIsNotNone(ml_service.features)

        print("✓ Backend MLService loaded model & features successfully")


if __name__ == "__main__":
    unittest.main()



## Run this file using git bash with this command """python -m tests.test_ml_api_integration"""
## You've got to run it this way with this specific command above or it probably might not run 