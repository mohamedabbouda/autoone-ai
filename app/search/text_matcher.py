
            


# app/search/text_matcher.py
from typing import List
from app.models.spare_part_model import SparePartModel

class TextMatcher:

    @staticmethod
    def score(tokens: List[str], part: SparePartModel) -> float:
        score = 0.0

        name = part.name.lower()
        desc = part.description.lower()

        for t in tokens:
            if t in name:
                score += 2.0
            if t in desc:
                score += 1.0
            if t == part.brand.lower():
                score += 1.5
            if t == part.category.lower():
                score += 1.0

        return score


