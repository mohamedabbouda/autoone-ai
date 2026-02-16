# app/features/feature_config.py
from pydantic import BaseModel

class FeatureConfig(BaseModel):
    """
    Feature choices for the recommendation engine.
    Keep it simple now; extend later when we have real data signals.
    """
    weight_rating: float = 2.0
    weight_distance: float = 1.0
    weight_open_now: float = 0.5  # small bonus when open

    # normalization defaults for mock data
    min_rating: float = 0.0
    max_rating: float = 5.0

    # if you don't know real-world bounds yet, set safe defaults
    max_distance_km: float = 25.0
    # output size
    max_results: int = 3
