import numpy as np
import pandas as pd

class VectorBuilder:
    def __init__(self, feature_index: dict):
        self.feature_index = feature_index
        self.n = len(feature_index)

    def build_vector(self, symptoms_list):
        v = np.zeros(self.n, dtype=int)
        for s in symptoms_list:
            idx = self.feature_index.get(s)
            if idx is not None:
                v[idx] = 1
        return v

    def dataset_to_matrix(self, df: pd.DataFrame, label_col='disease'):
        X = []
        y = []
        for _, r in df.iterrows():
            v = self.build_vector(r['symptoms'])
            X.append(v)
            y.append(r[label_col])
        X = np.vstack(X) if X else np.zeros((0, self.n), dtype=int)
        return X, y
