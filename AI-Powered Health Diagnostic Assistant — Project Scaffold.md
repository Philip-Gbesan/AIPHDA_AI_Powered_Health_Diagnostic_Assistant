# AI-Powered Health Diagnostic Assistant — Project Scaffold

This document is a developer-facing project scaffold and README for the AI-Powered Health Diagnostic Assistant. It contains:

* A clear, modular folder structure designed so any team-member’s component can be developed and swapped independently.
* A README explaining what the project does, how it works, and how to extend/replace components.
* Starter file templates and pointers for each major module.

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
AIPHDA_Health_Diagnostic_Assistant/
├── backend/
│   ├── __init__.py
│   ├── app.py                         # Flask app entrypoint
│   ├── routes/
│   |   ├── __init__.py
│   │   ├── predict.py                 # /predict and inference logic
│   │   ├── feedback.py                # /feddback and general advice
│   │   └── admin.py                   # /admin endpoints (upload CSV)
│   ├── services/
│   |   ├── __init__.py
│   │   └── ml_service.py           # model loading & wrapper for inference
│   ├── config.py                      # config (paths, DB URI, API keys)
│   └── app.py
│
├── database/
│   ├── db.py                          # database connection
│   ├── queries.py                     # database CRUD functions
|   ├── schema.sql                     # SQL schema for SQLite or MySQL
│   ├── seed.sql                       # seed data (basic diseases/symptoms)
│   ├── init_db.py                     # initialize and create database
│   └── dev.sqlite                     # optional dev DB
│
├── docs/
│   ├── AIPHDA_Project_Documentation.pdf # copy of PRD (or link to uploaded pdf)
│   ├── PRD.md                         # copy of PRD (or link to uploaded pdf)
│   └── Project DFD Diagram.png        # diagram (optional)
│
├── frontend/
│   ├── public/
│   │   ├── index.html                 # user symptom input + mic
│   │   ├── about.html                 # about page
│   │   ├── contact.html               # contact page
│   │   ├── admin.js                   # admin functionalities
│   │   └── admin.html                 # admin dashboard (basic)
│   └── README_frontend.md
│
├── ml/
├── ├── __init__.py
├── ├── preprocess/
│   ├── ├── __init__.py
│   ├── │
│   ├── ├── loaders/
│   ├── │   ├── __init__.py
│   ├── │   ├── base_loader.py
│   ├── │   ├── loader_binary_matrix.py
│   ├── │   ├── loader_symptom_list.py
│   ├── │   ├── loader_textual_description.py
│   ├── │   └── loader_auto.py
│   ├── │
│   ├── ├── cleaners/
│   ├── │   ├── __init__.py
│   ├── │   ├── normalize_text.py
│   ├── │   ├── symptom_cleaner.py
│   ├── │   ├── disease_cleaner.py
│   ├── │   └── synonyms_map.json
│   ├── │
│   ├── ├── merger/
│   ├── │   ├── __init__.py
│   ├── │   ├── dataset_merger.py
│   ├── │   ├── vector_builder.py
│   ├── │   └── feature_indexer.py
│   ├── │
│   ├── └── pipeline.py    # <--- Master pipeline (combines all modules)
├── ├── model/                         # model artifacts (joblib, metadata.json)
│   ├── ├── saved_model/
├── ├── data/
│   ├── ├── raw/          # datasets from Kaggle, Mendeley and others
│   ├── ├── processed/                     # master_dataset.csv + features.json
│   ├── │   ├── master_dataset.csv         # cleaned datasets used to train── public/
│   ├── │   └── features.json
├── ├── train.py
├── ├── evaluate.py
├── ├── requirements_ml.txt
├── ├── run_preprocess.py
├── ├── run_train_eval.py
├── ├── train.py
├── ├── utils.py
│
├── scripts/
│   ├── retrain.py                     # simple retrain script
│   ├── export_model.py                # package model artifacts
│   ├── preprocess_raw.py              # simple preprocess raw datasets script
│   ├── revert_model.py                # revert to model previous version
│   └── sync_data.py                   # admin upload helper
│
├── tests/
│   ├── __init__.py
│   ├── test_ml.py
│   ├── test_api.py
│   ├── test_ml_api_integration.py
│   ├── test_db.py
│   ├── test_scripts.py
│   └── test_frontend_integration.md
│
├── .gitignore
├── README.md                          # high-level README (see below)
└── CONTRIBUTING.md                    # how to contribute and code style
```

---


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


