-- MODELS TABLE
CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    path TEXT NOT NULL,
    accuracy REAL,
    top3_accuracy REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- FEATURES TABLE
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom TEXT NOT NULL,
    index_num INTEGER NOT NULL
);

-- USER FEEDBACK
CREATE TABLE IF NOT EXISTS user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_symptoms TEXT NOT NULL,
    predicted_condition TEXT NOT NULL,
    correct_condition TEXT,
    feedback TEXT CHECK (feedback IN ('accurate', 'inaccurate', 'uncertain')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ADMIN UPLOADED DATASETS
CREATE TABLE IF NOT EXISTS admin_uploaded_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    status TEXT CHECK (status IN ('pending','processed','invalid')),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- PREDICTION LOGS
CREATE TABLE IF NOT EXISTS prediction_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptoms TEXT NOT NULL,
    predictions TEXT NOT NULL,
    top_prediction TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- SYMPTOM TRENDS
CREATE TABLE IF NOT EXISTS symptom_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom TEXT NOT NULL,
    count INTEGER DEFAULT 0
);
