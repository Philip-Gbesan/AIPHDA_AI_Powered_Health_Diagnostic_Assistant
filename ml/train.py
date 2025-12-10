"""Train RandomForest with the processed master dataset."""
import joblib
import json
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from preprocess.merger.vector_builder import VectorBuilder
from preprocess.merger.feature_indexer import FeatureIndexer

def train(master_csv, features_json, out_model):
    df = pd.read_csv(master_csv)
    features = FeatureIndexer.load(features_json)
    vb = VectorBuilder(features)
    X, y = vb.dataset_to_matrix(df)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    clf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)
    clf.fit(X, y_enc)

    # save model, label encoder & metadata
    joblib.dump({'model': clf, 'label_encoder': le}, out_model)
    metadata = {
        'n_classes': int(len(le.classes_)),
        'classes': list(le.classes_)
    }
    with open(out_model + '.meta.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print('Saved model to', out_model)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--master_csv', default='ml/data/processed/master_dataset.csv')
    p.add_argument('--features_json', default='ml/data/processed/features.json')
    p.add_argument('--out', default='ml/model/rf_model.joblib')
    args = p.parse_args()
    train(args.master_csv, args.features_json, args.out)

