# small helpers
from typing import List

def ensure_list(x) -> List[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        return [s.strip() for s in x.replace(';', ',').split(',') if s.strip()]
    return list(x)
