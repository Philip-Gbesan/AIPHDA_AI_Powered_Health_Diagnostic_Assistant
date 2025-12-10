from .normalize_text import normalize_text

def clean_symptom(s: str, synonyms: dict):
    s = normalize_text(s)
    # apply synonyms mapping (exact match or simple membership)
    for canonical, syns in synonyms.items():
        if s == canonical or s in syns:
            return canonical
    return s
