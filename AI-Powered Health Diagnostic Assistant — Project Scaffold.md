# AI-Powered Health Diagnostic Assistant — Project Scaffold

This document is a developer-facing project scaffold and README for the AI-Powered Health Diagnostic Assistant. It contains:

* A clear, modular folder structure designed so any team-member’s component can be developed and swapped independently.
* A README explaining what the project does, how it works, and how to extend/replace components.
* Starter file templates and pointers for each major module.

> NOTE: Your original PRD file has been uploaded to the project folder path: `/mnt/data/AI-POWERED-HEALTH-DIAGNOSIS-ASSISTANT.pdf`. Use it as the authoritative requirements doc when developing features and tests.

---

## Project goals (short)

* Accept user symptoms via text or voice and return top-3 probable conditions with preventive advice.
* Admin interface for uploading/updating medical data and viewing analytics.
* Feedback loop: store anonymized user feedback for retraining.
* Modular single-repo layout so any component (ML, backend, frontend, DB, admin) can be replaced without large refactors.

---

## High-level architecture (modular)

* `ml/` — model training, preprocessing, tokenizer, model artifact output (joblib). *Swap-in/out here.*
* `backend/` — Flask API server that loads model artifacts and serves prediction + admin endpoints.
* `frontend/` — Static HTML + Tailwind + JS for user-facing pages and admin dashboard (simple, replaceable).
* `db/` — DB migrations & example SQLite DB used for dev.
* `data/` — raw and processed datasets, CSVs used for training.
* `scripts/` — helper scripts (retrain, evaluate, export).
* `docs/` — PRD, architecture diagrams, and developer notes.
* `tests/` — unit/integration tests for each module.

---

## Folder structure (recommended)

```
ai-health-assistant/
├── ml/
│   ├── data_preprocessing.py          # text cleaning, tokenization, mapping to symptom IDs
│   ├── feature_engineering.py         # build symptom vectors
│   ├── train.py                       # train RandomForest, save model joblib
│   ├── evaluate.py                    # evaluation metrics, top-3 accuracy
│   ├── model/                         # model artifacts (joblib, metadata.json)
│   └── requirements-ml.txt            # ML-specific dependencies
├── backend/
│   ├── app.py                         # Flask app entrypoint
│   ├── api/
│   │   ├── predict.py                 # /predict and inference logic
│   │   ├── audio.py                   # audio->text integration (Vosk wrapper)
│   │   └── admin.py                   # /admin endpoints (upload CSV)
│   ├── services/
│   │   ├── model_service.py           # model loading & wrapper for inference
│   │   └── db_service.py              # DB access functions
│   ├── config.py                      # config (paths, DB URI, API keys)
│   ├── requirements.txt
│   └── Dockerfile                     # optional local dev container
├── frontend/
│   ├── public/
│   │   ├── index.html                 # user symptom input + mic
│   │   ├── results.html               # results + feedback UI
│   │   └── admin.html                 # admin dashboard (basic)
│   ├── static/
│   │   ├── app.js                     # frontend fetch requests
│   │   └── styles.css                 # Tailwind compiled styles or link
│   └── README_frontend.md
├── db/
│   ├── schema.sql                     # SQL schema for SQLite or MySQL
│   ├── seed.sql                       # seed data (basic diseases/symptoms)
│   └── dev.sqlite                     # optional dev DB
├── data/
│   ├── raw/                           # original datasets (CSV, JSON)
│   └── processed/                     # cleaned datasets used to train
├── scripts/
│   ├── retrain.sh                     # simple retrain script
│   ├── export_model.sh                # package model artifacts
│   └── sync_data.sh                   # admin upload helper
├── docs/
│   ├── PRD.md                         # copy of PRD (or link to uploaded pdf)
│   └── architecture.png               # diagram (optional)
├── tests/
│   ├── test_ml.py
│   ├── test_api.py
│   └── test_frontend_integration.md
├── .gitignore
├── README.md                          # high-level README (see below)
└── CONTRIBUTING.md                    # how to contribute and code style
```

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

















ml/
├── preprocess/
│   ├── __init__.py
│   │
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── base_loader.py
│   │   ├── loader_binary_matrix.py
│   │   ├── loader_symptom_list.py
│   │   ├── loader_textual_description.py
│   │   └── loader_auto.py
│   │
│   ├── cleaners/
│   │   ├── __init__.py
│   │   ├── normalize_text.py
│   │   ├── symptom_cleaner.py
│   │   ├── disease_cleaner.py
│   │   └── synonyms_map.json
│   │
│   ├── merger/
│   │   ├── __init__.py
│   │   ├── dataset_merger.py
│   │   ├── vector_builder.py
│   │   └── feature_indexer.py
│   │
│   └── pipeline.py    # <--- Master pipeline (combines all modules)
│
├── train.py
├── evaluate.py
├── utils.py
│
└── data/
    ├── raw/          # datasets from Kaggle, Mendeley
    ├── staged/       # cleaned not-yet-merged datasets
    └── processed/    # master_dataset.csv + features.json



database/
│── dev.sqlite          <-- your development database
│── schema.sql          <-- table creation SQL file
│── seed.sql            <-- initial seed data (optional)
│── migrate.sql         <-- future migration scripts (optional)
│── init_db.py          <-- python script to bootstrap DB from schema.sql
│── db.py               <-- connection helper
│── queries.py          <-- reusable DB functions



backend/
│── __init__.py
│── app.py
│── config.py
│── routes/
│     ├── __init__.py
│     ├── predict.py
│     ├── feedback.py
│     ├── admin.py
│
│── services/
│     ├── __init__.py
│     ├── ml_service.py
│     ├── advice_service.py
│
│── utils/
│     ├── __init__.py
│     ├── loader.py
│
