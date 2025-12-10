
---

## README.md (developer + user friendly)

> The README below is the file that will live at the project root. It explains the project, how to run it locally, where to find modules, and how to swap components.

### README.md (summary)

```
# AI-Powered Health Diagnostic Assistant

A modular prototype that accepts symptom input (text or voice), predicts the top-3 probable conditions using an ML model (RandomForest by default), and provides preventive advice. The project is designed for local development and easy component replacement.

## Project layout
(See folder structure in docs/ for full details.)

## Quick start (dev)
1. Clone repo
2. Create virtualenv: `python -m venv .venv && source .venv/bin/activate`
3. Install backend deps: `cd backend && pip install -r requirements.txt`
4. Install ML deps: `cd ../ml && pip install -r requirements-ml.txt`
5. Prepare DB:
   - `sqlite3 db/dev.sqlite < db/schema.sql`
   - run seed: `sqlite3 db/dev.sqlite < db/seed.sql`
6. Train a quick model (optional if model artifact exists): `python ml/train.py --data data/processed/train.csv --out ml/model/rf_v1.joblib`
7. Start Flask backend: `cd backend && FLASK_APP=app.py flask run`
8. Open `frontend/public/index.html` in browser (or serve via simple HTTP server)

## How to swap components
- Replace ML model: output `joblib` model into `ml/model/` and update `model_service.py` path in backend/config.
- Replace frontend: keep API contract (POST /predict returns predicted array of {disease, prob, preventive}) and any UI can be plugged in.
- Replace DB: update `db_service.py` interface; backend uses db_service functions (CRUD) only — keep same function signatures.

## API endpoints (summary)
- `POST /api/v1/predict` - JSON {text, age?, sex?} => top-3 predictions
- `POST /api/v1/predict/audio` - multipart audio upload
- `POST /api/v1/feedback` - store user feedback
- `POST /api/v1/admin/upload` - admin CSV upload

## Notes & ethics
- This prototype is not a medical device and does NOT replace professional medical advice.
- Keep user data anonymous. Do not store identifiable PII.

## Contributing
See CONTRIBUTING.md for coding style, branch strategy, and PR checks.
```

---

## Guidelines for making each component replaceable

1. **Define clear interfaces** — each module exposes a small surface area:

   * `model_service.predict(symptom_vector)` returns a list of (disease_id, prob)
   * `db_service.get_preventive_text(disease_id)` returns text
   * `audio_service.transcribe(audio_bytes)` returns plain text
   * `nlp_service.extract_symptoms(raw_text)` returns symptom_vector

2. **Keep configs in `backend/config.py`** — file paths, DB URI, model path, external API keys. When swapping modules only update config.

3. **Model artifact contract** — the model must accept a fixed-size feature vector (same order of symptoms). Keep a `features.json` in `ml/model/` describing symptom list order.

4. **Use dependency injection in backend** — `ModelService(model_path, features_json)` so you can replace with another model implementation easily.

---

## Starter templates (short pointers)

* `ml/train.py` should produce: `ml/model/rf_v1.joblib` and `ml/model/metadata.json` containing symptoms order.
* `backend/services/model_service.py` should read `metadata.json` to map extracted symptoms into the model feature order.
* `frontend/static/app.js` should expect `{predictions: [{disease, prob, preventive}]}` from `POST /api/v1/predict`.

---

## Testing & QA

* Add `tests/test_api.py` to simulate a POST /predict with canned symptom text and assert the response has top-3.
* `tests/test_ml.py` should check `train.py` produces a model and that top-3 accuracy > baseline.

