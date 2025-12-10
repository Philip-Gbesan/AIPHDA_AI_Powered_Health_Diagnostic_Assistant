# CONTRIBUTING.md

# 🧬 AI-Powered Health Diagnostic Assistant — Contribution Guide

Thank you for considering contributing to the **AI-Powered Health Diagnostic Assistant**.
This project is designed with a **modular architecture**, allowing each core component (ML model, backend API, frontend UI, database layer, admin dashboard) to be independently developed and replaced.

This guide covers:

* How the project is structured
* Developer setup
* Coding standards
* Git workflow
* How to replace parts of the system easily
* Testing instructions

---

# 📁 Project Structure

```
ai-health-assistant/
├── ml/                     # Machine learning pipeline
├── backend/                # Flask API backend
├── frontend/               # HTML/Tailwind/JS user interface
├── db/                     # Schema, migrations, seed data
├── data/                   # Raw + processed datasets
├── docs/                   # PRD, diagrams, architecture
├── scripts/                # Utility scripts (retrain, export)
├── tests/                  # Unit & integration tests
└── README.md
```

Each folder is isolated so contributors can work without interfering with other parts of the system.

---

# 🧩 Contribution Areas

### **1. Machine Learning (ml/)**

* Dataset sourcing, cleaning & preprocessing
* NLP symptom extraction
* RandomForest model development
* Model evaluation (accuracy, top-3 accuracy)
* Exporting model artifacts (`.joblib`, `metadata.json`)

---

### **2. Backend API (backend/)**

* Flask routing & controller logic
* Loading ML model artifacts
* Input validation & error handling
* Audio → text pipeline (Vosk or external API)
* Mapping predictions to preventive measures

---

### **3. Database Layer (db/)**

* Designing SQL schema
* Writing SQL CRUD operations
* Integrating DB functions with backend services
* Admin data ingestion

---

### **4. Frontend UI (frontend/)**

* Symptom input UI
* Voice input uploading
* Results page & feedback UI
* Admin dashboard UI
* Tailwind styling
* Fetch API integration

---

### **5. Admin Dashboard / Analytics**

* Displaying model accuracy
* Displaying symptom trends
* Dataset upload UI
* Optional JS charts

---

# 🚀 Getting Started

### **1. Clone the Repository**

```bash
git clone https://github.com/<your-org>/ai-health-assistant.git
cd ai-health-assistant
```

---

### **2. Create a Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

---

### **3. Install Backend Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

---

### **4. Install ML Dependencies**

```bash
cd ../ml
pip install -r requirements-ml.txt
```

---

### **5. Set Up the Database**

```bash
sqlite3 db/dev.sqlite < db/schema.sql
sqlite3 db/dev.sqlite < db/seed.sql
```

---

### **6. Train a Model (Optional if a model exists)**

```bash
python ml/train.py --data data/processed/train.csv --out ml/model/rf_v1.joblib
```

---

### **7. Start the Flask Backend**

```bash
cd backend
flask --app app.py run
```

---

### **8. Launch the Frontend**

Open:

```
frontend/public/index.html
```

(or use a simple live server)

---

# 🧪 Testing

Tests are located in the **tests/** directory.

Run everything:

```bash
pytest
```

Run specific tests:

```bash
pytest tests/test_api.py
pytest tests/test_ml.py
```

---

# 🔧 Coding Standards

### **Python**

* Follow **PEP 8** style guidelines
* Use descriptive function names + docstrings
* Keep business logic separate from route handlers
* Every trained model must include:

  * `model.joblib`
  * `metadata.json` (feature order, accuracy, version)

### **JavaScript**

* Use modern ES6+ syntax
* Keep API logic in `frontend/static/app.js`
* Avoid inline JS in HTML files

### **HTML / Tailwind**

* Keep class usage clean and meaningful
* Avoid embedding large scripts directly in HTML

---

# 🔀 Git Workflow

This project uses a **feature-branch workflow**.

### **1. Create a feature branch**

```bash
git checkout -b feature/<task-name>
```

Examples:

```
feature/ml-model-training
feature/frontend-results-page
feature/api-audio-endpoint
```

### **2. Commit frequently**

```bash
git commit -m "Implemented symptom vectorizer"
```

### **3. Push your branch**

```bash
git push origin feature/<task-name>
```

### **4. Create a Pull Request**

* Provide clear summary
* Link to related issue/task
* Include any test results
* Add screenshots if UI-related

---

# 📦 Replacing System Components (Modular Architecture)

This project is designed so **any part can be replaced** with minimal friction.

### **Replacing the ML Model**

Just ensure:

* A `.joblib` file is output
* Matching `metadata.json` exists
* Backend’s `ModelService.predict()` interface stays intact

### **Replacing the Frontend**

Frontend only needs to call:

* `POST /api/v1/predict`
* `POST /api/v1/feedback`
* `POST /api/v1/admin/upload`

Any framework (React, Vue, Svelte, plain HTML) can replace the default UI.

### **Replacing the Database**

Update internal logic inside `db_service.py`.
As long as function signatures remain unchanged, backend code will continue working.

---

# 💬 Communication & Collaboration

* Use GitHub Issues for discussions and bug reports
* Keep PR titles & commit messages descriptive
* Do **not** push to `main` directly
* Document new functions, routes, or components
* Avoid breaking API contracts without discussion

---

# 🛡️ Ethical Notice

This system is **NOT** a medical device.
It does **not** provide real medical diagnoses.

* Never store personal identifying information
* Keep user data anonymous
* Include disclaimers in UI and documentation

---

# 🤝 Thank You for Contributing!

Your contributions help improve this educational and practical AI-powered prototype.
If you have questions or suggestions, please open an issue or start a discussion.
