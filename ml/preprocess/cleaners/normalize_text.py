import re

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ''
    text = text.lower()
    # remove unicode weirdness and extra whitespace
    text = re.sub(r"\s+", ' ', text)
    text = re.sub(r"[^a-z0-9,.;:\/\-\(\) ]+", '', text)
    return text.strip()
