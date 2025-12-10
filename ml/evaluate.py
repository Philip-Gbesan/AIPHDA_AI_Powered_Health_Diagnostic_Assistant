import json
import argparse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from preprocess.merger.vector_builder import VectorBuilder
from preprocess.merger.feature_indexer import FeatureIndexer
import numpy as np

def top_k_accuracy(clf, X, y_true, k=3):
    proba = clf.predict_proba(X)
    topk = np.argsort(proba, axis=1)[:, ::-1][:, :k]
    correct = 0
    for i, row in enumerate(topk):
        if y_true[i] in row:
            correct += 1
    return correct / len(y_true)

def evaluate(master_csv, features_json, model_path):
    df = pd.read_csv(master_csv)
    features = FeatureIndexer.load(features_json)
    vb = VectorBuilder(features)
    X, y = vb.dataset_to_matrix(df)

    # load model
    obj = joblib.load(model_path)
    clf = obj['model']
    le = obj['label_encoder']
    y_enc = le.transform(y)

    acc = accuracy_score(y_enc, clf.predict(X))
    top3 = top_k_accuracy(clf, X, y_enc, k=3)

    res = {'accuracy': float(acc), 'top3_accuracy': float(top3)}
    print(json.dumps(res, indent=2))
    with open(model_path + '.eval.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--master_csv', default='ml/data/processed/master_dataset.csv')
    p.add_argument('--features_json', default='ml/data/processed/features.json')
    p.add_argument('--model', default='ml/model/rf_model.joblib')
    args = p.parse_args()
    evaluate(args.master_csv, args.features_json, args.model)
