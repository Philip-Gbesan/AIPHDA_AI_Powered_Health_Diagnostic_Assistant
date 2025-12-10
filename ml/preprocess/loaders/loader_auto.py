"""Auto-detect loader based on columns and content."""
import pandas as pd
from .loader_symptom_list import SymptomListLoader
from .loader_binary_matrix import BinaryMatrixLoader
from .loader_textual_description import TextualDescriptionLoader
from .base_loader import BaseLoader

class AutoLoader(BaseLoader):
    def load(self, path: str):
        df = pd.read_csv(path, nrows=5)
        cols = [c.lower() for c in df.columns]
        # if many columns and binary-like -> binary loader
        # crude check: if dataframe values contain many 0/1 strings
        flattened = df.astype(str).values.flatten()
        if len(cols) > 5 and any(x in ('0','1') for x in flattened):
            loader = BinaryMatrixLoader(self.synonyms)
        elif 'description' in cols or 'text' in cols or 'clinical_notes' in cols:
            loader = TextualDescriptionLoader(self.synonyms)
        else:
            loader = SymptomListLoader(self.synonyms)
        return loader.load(path)
