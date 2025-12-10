from .normalize_text import normalize_text

def clean_disease(d: str):
    d = normalize_text(d)
    # basic normalization - more rules can be added
    d = d.replace('disease', '').strip()
    return d
