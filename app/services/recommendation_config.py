# app/services/recommendation_config.py

class RecommendationConfig:
    """
    Configuration for recommendation scoring.
    Easy to tune or replace with ML later.
    """

    rating_weight: float = 2.0
    distance_weight: float = 1.0
    max_results: int = 3
