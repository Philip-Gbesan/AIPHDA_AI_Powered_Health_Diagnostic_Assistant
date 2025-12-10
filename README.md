
---

## README.md (developer + user friendly)

> The README below is the .md file at the project root. It explains the project, how to run it locally, where to find modules, and how to swap components.

### README.md (summary)

```
# AI-Powered Health Diagnostic Assistant

A modular prototype that accepts symptom input (text or voice), predicts the top-3 probable conditions using an ML model (RandomForest by default), and provides general preventive advice and reccomendations. The project is designed for local development and easy component replacement.

## Project layout
(See folder structure in docs/ for full details.)

## Quick start (dev)
1. Clone repo "https://github.com/Philip-Gbesan/AIPHDA_AI_Powered_Health_Diagnostic_Assistant"
2. Create virtualenv: `python -m venv .venv && source .venv/bin/activate`
3. Install backend deps: `cd backend && pip install -r requirements.txt`
4. Install ML deps: `cd ../ml && pip install -r requirements-ml.txt`
5. Prepare DB:
   - `sqlite3 database/dev.sqlite < database/schema.sql`
   - run init file: `database/init_db.py`
6. Train a quick model (optional if model artifact exists): `python ml/train.py --data data/processed/train.csv --out ml/model/rf_v1.joblib`
7. Start Flask backend: `python -m backend.app`
8. Run `python -m http.server 5000` and then open `http://localhost:5000/frontend/public/index.html` in browser (DO not serve via simple HTTP server or live server else backend would keep on reloading whenever any backend post or fetch requests are made)
9. Make sure both the backend and the frontend are run in different terminal and are both running else the program won't run

## How to swap components
- Replace ML model: output `joblib` model into `ml/model/` and update `ml_service.py` path in backend/config.
- Replace frontend: keep API contract (POST /predict returns predicted array of {disease, prob, preventive}) and any UI can be plugged in.
- Replace DB: update `queries.py` and the `schema.sql` interface; backend uses `queries.py` functions (CRUD) only — keep same function signatures.

## API endpoints (summary)
- `POST /api/predict` - JSON {text, age?, sex?} => top-3 predictions
- `POST /api/feedback` - stores user feedback
- `GET /api/admin/logs` - admin stats logs
- `GET /api/admin/download-model` - admin download current model
- `POST /api/admin/upload-dataset` - admin upload raw training Dataset in .csv format
- `POST /api/admin/preprocess` - admin preprocess raw Datasets to Master Dataset
- `POST /api/admin/retrain` - admin retrain model on Master Dataset
- `POST /api/admin/revert-model` - admin revert model to previous version

## Notes & ethics
- This prototype is not a medical device and does NOT replace professional medical advice.
- Keep user data anonymous. Do not store identifiable PII.

## Contributing
See CONTRIBUTING.md for coding style, branch strategy, and PR checks.
```

---

## Guidelines for making each component replaceable

1. **Define clear interfaces** — each module exposes a small surface area:

   * `ml_service.predict(symptom_vector)` returns a list of (disease_id, prob)
   * `db_service.get_preventive_text(disease_id)` returns text
   * `nlp_service.extract_symptoms(raw_text)` returns symptom_vector

2. **Keep configs in `backend/config.py`** — file paths, DB URI, model path, external API keys. When swapping modules only update config.

3. **Model artifact contract** — the model must accept a fixed-size feature vector (same order of symptoms). Keep a `features.json` in `ml/model/` describing symptom list order.

4. **Use dependency injection in backend** — `MLService(model_path, features_json)` so you can replace with another model implementation easily.

---

## Starter templates (short pointers)

* `ml/train.py` should produce: `ml/model/rf_v1.joblib` and `ml/model/metadata.json` containing symptoms order.
* `backend/services/ml_service.py` should read `metadata.json` to map extracted symptoms into the model feature order.
* `frontend/public/index.html` with its script should expect `{predictions: [{disease, prob, preventive}]}` from `POST /api/predict`.

---

## Testing & QA

* Add `tests/test_api.py` to simulate a POST /predict with canned symptom text and assert the response has top-3.
* `tests/test_ml.py` should check `train.py` produces a model and that top-3 accuracy > baseline.
* `tests/test_ml_api.py` should check that the ML and APIs integrate seamlessly to give back results while handling all errors.
* `tests/test_frontend_integration` should check that the frontend interface integrates properly with the backend 
* `tests/test_db.py` should check `init_db.py` produces the database and that all the functions work and perform CRUD operations on the database.
* `tests/test_scripts.py` should check `scripts/` that all the scripts files actually works.

