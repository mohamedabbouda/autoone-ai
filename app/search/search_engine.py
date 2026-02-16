# app/search/search_engine.py
from typing import List,Optional
from app.search.tokenizer import tokenize
from app.search.text_matcher import TextMatcher
from app.models.spare_part_model import SparePartModel

class SparePartSearchEngine:

    def __init__(self, parts: List[SparePartModel]):
        self.parts = parts

    def search(self, query: str,limit: Optional[int] = None) -> List[SparePartModel]:

        tokens = tokenize(query)

        scored = []
        for part in self.parts:
            s = TextMatcher.score(tokens, part)
            if s > 0:
                part.score = s
                scored.append(part)

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]





