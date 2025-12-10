"""
API Test Suite for AI Health Diagnostic Assistant Backend

This script tests:
- /api/predict
- /api/feedback
- /api/admin/upload-dataset
- /api/admin/datasets
- /api/admin/models
- /api/admin/logs
- /api/admin/symptom-trends

Run using:
    python -m tests.test_api
"""

import io
import json
import unittest
from backend.app import create_app


class APITestCase(unittest.TestCase):

    def setUp(self):
        """Create Flask test client"""
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    # ---------------------------------------
    # PREDICT
    # ---------------------------------------
    def test_predict(self):
        response = self.client.post(
            "/api/predict",
            json={"symptoms": ["fever", "cough"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn("predictions", data)
        self.assertGreater(len(data["predictions"]), 0)
        print("\n✓ /api/predict OK")

    # ---------------------------------------
    # FEEDBACK
    # ---------------------------------------
    def test_feedback(self):
        response = self.client.post(
            "/api/feedback",
            json={
                "symptoms": ["fever", "cough"],
                "predicted": "flu",
                "feedback": "accurate"
            }
        )

        self.assertEqual(response.status_code, 200)
        print("✓ /api/feedback OK")

    # ---------------------------------------
    # ADMIN: UPLOAD DATASET
    # ---------------------------------------
    def test_upload_dataset(self):
        data = {
            "file": (io.BytesIO(b"column1,column2\nval1,val2"), "test.csv")
        }

        response = self.client.post(
            "/api/admin/upload-dataset",
            content_type="multipart/form-data",
            data=data
        )

        self.assertEqual(response.status_code, 200)
        print("✓ /api/admin/upload-dataset OK")

    # ---------------------------------------
    # ADMIN: LIST DATASETS
    # ---------------------------------------
    def test_list_datasets(self):
        response = self.client.get("/api/admin/datasets")
        self.assertEqual(response.status_code, 200)
        print("✓ /api/admin/datasets OK")

    # ---------------------------------------
    # ADMIN: LIST MODELS
    # ---------------------------------------
    def test_list_models(self):
        response = self.client.get("/api/admin/models")
        self.assertEqual(response.status_code, 200)
        print("✓ /api/admin/models OK")

    # ---------------------------------------
    # ADMIN: PREDICTION LOGS
    # ---------------------------------------
    def test_logs(self):
        response = self.client.get("/api/admin/logs")
        self.assertEqual(response.status_code, 200)
        print("✓ /api/admin/logs OK")

    # ---------------------------------------
    # ADMIN: SYMPTOM TRENDS
    # ---------------------------------------
    def test_symptom_trends(self):
        response = self.client.get("/api/admin/symptom-trends")
        self.assertEqual(response.status_code, 200)
        print("✓ /api/admin/symptom-trends OK")


if __name__ == "__main__":
    unittest.main()


## Run this file using git bash with this command """python -m tests.test_api"""
## You've got to run it this way with this specific command above or it probably might not run 