# app/features/feature_builder.py
from __future__ import annotations

from app.features.feature_config import FeatureConfig
from app.features.normalizer import FeatureNormalizer
from app.models.service_model import ServiceModel

class FeatureBuilder:
    """
    Turns a ServiceModel into numeric features for scoring (and later ML training).
    """

    def __init__(self, config: FeatureConfig):
        self.config = config

    def build(self, service: ServiceModel) -> dict[str, float]:
        """
        Requires the engine to have already computed:
          - service.distance_km
          - service.is_available
        """
        rating_norm = FeatureNormalizer.min_max(
            service.rating,
            self.config.min_rating,
            self.config.max_rating
        )

        distance_closeness = FeatureNormalizer.distance_to_score(
            service.distance_km or self.config.max_distance_km,
            self.config.max_distance_km
        )

        open_now = 1.0 if service.is_available else 0.0

        return {
            "rating_norm": rating_norm,
            "distance_closeness": distance_closeness,
            "open_now": open_now,
        }
