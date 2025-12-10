import pandas as pd
from .base_loader import BaseLoader

class BinaryMatrixLoader(BaseLoader):
    """Loads datasets where each symptom is a column with binary 0/1 values and one disease column."""
    def load(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        cols = df.columns.tolist()
        # guess disease column
        disease_col = None
        for c in cols:
            if c.lower() in ('disease', 'disease_name', 'diagnosis'):
                disease_col = c
                break
        if disease_col is None:
            disease_col = cols[0]
        symptom_cols = [c for c in cols if c != disease_col]

        records = []
        for _, row in df.iterrows():
            disease = str(row[disease_col]).strip()
            symptoms = [s for s in symptom_cols if str(row[s]) not in ('0', '0.0', 'False', 'false', '')]
            records.append({'disease': disease, 'symptoms': symptoms})
        return pd.DataFrame(records)
