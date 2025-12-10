"""Master preprocessing pipeline.
Run as: python -m ml.preprocess.pipeline --raw_dir ml/data/raw --out_dir ml/data/processed
"""
import argparse
import json
from pathlib import Path
from preprocess.loaders.loader_auto import AutoLoader
from preprocess.merger.dataset_merger import DatasetMerger

def main(raw_dir: str, out_dir: str, synonyms_path: str):
    raw_dir = Path(raw_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load synonyms
    with open(synonyms_path, 'r', encoding='utf-8') as f:
        synonyms = json.load(f)

    loader = AutoLoader(synonyms=synonyms)
    staged = []

    for csv in raw_dir.glob('*.csv'):
        print('Loading', csv)
        df = loader.load(csv)
        staged.append((csv.name, df))

    merger = DatasetMerger(synonyms=synonyms)
    master_df, feature_index = merger.merge(staged)

    # save master dataset and features
    master_csv = out_dir / 'master_dataset.csv'
    features_json = out_dir / 'features.json'

    master_df.to_csv(master_csv, index=False)
    with open(features_json, 'w', encoding='utf-8') as f:
        json.dump(feature_index, f, ensure_ascii=False, indent=2)

    print('Saved master dataset to', master_csv)
    print('Saved features to', features_json)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--raw_dir', default='ml/data/raw')
    p.add_argument('--out_dir', default='ml/data/processed')
    p.add_argument('--synonyms', default='ml/preprocess/cleaners/synonyms_map.json')
    args = p.parse_args()
    main(args.raw_dir, args.out_dir, args.synonyms)
