# app/search/tokenizer.py
import re
from typing import List

def tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return [t for t in text.split() if len(t) > 1]
