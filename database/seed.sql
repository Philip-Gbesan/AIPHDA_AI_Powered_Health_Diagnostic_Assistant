INSERT INTO models (version, path, accuracy, top3_accuracy)
VALUES ('v0', 'ml/model/rf_model.joblib', 0.0, 0.0);

INSERT INTO symptom_trends (symptom, count) VALUES
('fever', 10),
('cough', 5),
('headache', 3);
