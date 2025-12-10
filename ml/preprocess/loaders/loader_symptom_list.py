import pandas as pd
from .base_loader import BaseLoader

class SymptomListLoader(BaseLoader):
    """Loads datasets with columns like 'Disease' and 'Symptoms' where Symptoms is a delimiter-separated list."""
    def load(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        # find likely columns
        cols = {c.lower(): c for c in df.columns}
        disease_col = cols.get('disease') or cols.get('disease_name') or list(df.columns)[0]
        # find symptoms column
        symptoms_col = None
        for key in ['symptoms', 'symptom', 'symptom_list', 'symptom(s)', 'description']:
            if key in cols:
                symptoms_col = cols[key]
                break
        if symptoms_col is None:
            # pick second column
            symptoms_col = list(df.columns)[1] if len(df.columns) > 1 else None

        records = []
        for _, row in df.iterrows():
            disease = str(row[disease_col]).strip()
            raw = ''
            if symptoms_col:
                raw = str(row[symptoms_col])
            # split common delimiters
            parts = [s.strip() for s in str(raw).replace(';', ',').replace('/', ',').split(',') if s.strip()]
            records.append({'disease': disease, 'symptoms': parts})

        return pd.DataFrame(records)
