import pandas as pd
from .base_loader import BaseLoader
from ..cleaners.normalize_text import normalize_text

class TextualDescriptionLoader(BaseLoader):
    """Loads datasets that have free-text descriptions. Attempts simple sentence splitting to find symptoms."""
    def load(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        # heuristics to find disease & description columns
        cols = {c.lower(): c for c in df.columns}
        disease_col = cols.get('disease') or cols.get('diagnosis') or list(df.columns)[0]
        desc_col = None
        for key in ['description', 'symptoms', 'clinical_notes', 'text']:
            if key in cols:
                desc_col = cols[key]
                break
        if desc_col is None:
            desc_col = list(df.columns)[1] if len(df.columns) > 1 else None

        records = []
        for _, row in df.iterrows():
            disease = str(row[disease_col]).strip()
            raw = ''
            if desc_col:
                raw = str(row[desc_col])
            # use simple normalization and split on punctuation
            text = normalize_text(raw)
            tokens = [t.strip() for t in text.replace(';', '.').split('.') if t.strip()]
            # assume sentences that contain common symptom keywords are symptoms
            records.append({'disease': disease, 'symptoms': tokens})
        return pd.DataFrame(records)
