# AI-Powered Health Diagnostic Assistant — Product Requirements Document (PRD)

## 1. Overview

The **AI-Powered Health Diagnostic Assistant** is an intelligent system designed to help users understand potential health conditions based on their symptoms. Users can interact with the system via text or voice. The system analyzes symptoms using Natural Language Processing (NLP), classifies possible medical conditions using a trained machine learning model, and provides the top 3 most probable conditions along with preventive measures.

This is an educational, research-focused system and **not a medical diagnostic tool**.

---

## 2. Goals & Objectives

### Primary Goals

* Allow users to enter symptoms via text or voice.
* Predict the **top 3 most likely health conditions**.
* Provide preventive measures for each suggested condition.
* Allow administrators to upload/update datasets and view analytics.
* Support continuous model improvement via user feedback.

### Secondary Goals

* Provide location-based suggestions for nearest hospitals/clinics.
* Maintain full modularity so components can be independently replaced.

---

## 3. Users

### **End Users (Patients/Individuals)**

* Input symptoms and receive possible conditions.
* Get preventive advice or suggestions.
* Submit feedback on the prediction accuracy.

### **System Administrators**

* Upload or modify medical datasets.
* View analytics (model accuracy, symptom trends).
* Trigger retraining or update model artifacts.

---

## 4. System Features

### 4.1 Symptom Input

* **Text Input**: Users type symptoms into the UI.
* **Voice Input**: User uploads audio → converted to text via STT (Vosk/API).

### 4.2 NLP Engine

* Extracts medical symptoms from raw user text.
* Maps symptoms to standardized IDs.
* Generates feature vectors used by the classification model.

### 4.3 Disease Prediction Engine

* Uses Random Forest classifier.
* Outputs: Top-3 predicted diseases + confidence scores.
* Uses metadata for symptom vector ordering.

### 4.4 Preventive Measures

* Each predicted disease is mapped to advice such as:

  * Home remedies
  * Lifestyle adjustments
  * When to seek a doctor

### 4.5 Feedback Loop

* Users can indicate if the prediction was helpful.
* Optional: Specify correct disease if known.
* Stored anonymously for retraining.

### 4.6 Admin Dashboard

* Upload new medical datasets.
* View analytics:

  * Symptom trends
  * Prediction accuracy
  * Dataset growth

### 4.7 Hospital/Clinic Suggestions

* Integrates with a location API.
* Returns nearest healthcare facilities.

---

## 5. Functional Requirements

### 5.1 User Interface (Frontend)

* HTML + Tailwind UI.
* Voice recording button.
* Display 3 predicted conditions with probabilities.
* Feedback UI.

### 5.2 Backend (Flask)

* `/predict` – Accepts text, returns predictions.
* `/feedback` – Stores user feedback.
* `/admin/upload` – Dataset upload.

### 5.3 Machine Learning

* RandomForest classifier.
* Uses preprocessing pipeline.
* Exports model as `.joblib`.

---

## 6. Non-Functional Requirements

* **Performance**: Prediction < 3 seconds.
* **Accuracy**: Target top-3 accuracy > 70%.
* **Scalability**: Modular design for easy upgrades.
* **Security**: No personal data stored.
* **Portability**: Should run on local machines for demo.

---

## 7. Tech Stack

**Machine Learning**: Python, Scikit-learn, SpaCy, NLTK
**Backend**: Flask, Python
**Frontend**: HTML, Vanila CSS, JavaScript
**Database**: SQLite
**Voice-to-Text**: Vosk or External API

---

# Architecture Diagram (architecture.png)

Below is the **ASCII version** of the system architecture.
You can export this into any diagram tool later to produce `architecture.png`.

```
                 ┌───────────────────────────┐
                 │        FRONTEND UI        │
                 │  - HTML/CSS               │
User Input  ---> │  - JS (fetch API)         │ ---> Feedback
 Voice/Text       └─────────────┬─────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │      BACKEND        │
                      │      (Flask)        │
                      ├─────────────────────┤
                      │ /predict            │
                      │ /predict/audio      │
                      │ /feedback           │
                      │ /admin/upload       │
                      └──────────┬──────────┘
                                 │
                                 ▼
                     ┌──────────────────────┐
                     │   NLP ENGINE         │
                     │ - Text cleaning       │
                     │ - Symptom extraction  │
                     │ - Vectorization       │
                     └──────────┬───────────┘
                                │ Feature Vector
                                ▼
                 ┌────────────────────────────────┐
                 │        ML MODEL SERVICE        │
                 │  - RandomForestClassifier      │
                 │  - model.joblib + metadata     │
                 └───────────┬────────────────────┘
                             │ Predictions (Top-3)
                             ▼
                 ┌────────────────────────────────┐
                 │  PREVENTIVE ADVICE SERVICE     │
                 │  Maps disease → advice         │
                 └────────────────────────────────┘

                    ▲                           
                    │ Writes feedback            
                    │ Updates datasets            
                    │                            
             ┌────────────────────────┐         
             │        DATABASE         │         
             │   SQLite / MySQL        │         
             │ - symptoms              │         
             │ - diseases              │         
             │ - feedback              │         
             │ - training_examples     │         
             └────────────────────────┘         

```

---

## End of PRD + Architecture Document
