"""Base loader interface."""
from abc import ABC, abstractmethod
import pandas as pd

class BaseLoader(ABC):
    def __init__(self, synonyms=None):
        self.synonyms = synonyms or {}

    @abstractmethod
    def load(self, path: str) -> pd.DataFrame:
        """Load raw file and return DataFrame with columns: disease, symptoms (list)"""
        raise NotImplementedError
