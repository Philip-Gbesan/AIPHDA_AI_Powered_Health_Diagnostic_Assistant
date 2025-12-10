import json

class FeatureIndexer:
    @staticmethod
    def save(feature_index: dict, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(feature_index, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
