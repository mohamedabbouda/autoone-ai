# app/features/normalizer.py
from __future__ import annotations

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

class FeatureNormalizer:
    """
    Normalizes raw values into 0..1 for ML readiness.
    Min-max scaling is a standard starting point. :contentReference[oaicite:2]{index=2}
    """

    @staticmethod
    def min_max(value: float, vmin: float, vmax: float) -> float:
        if vmax <= vmin:
            return 0.0
        return clamp((value - vmin) / (vmax - vmin), 0.0, 1.0)

    @staticmethod
    def distance_to_score(distance_km: float, max_distance_km: float) -> float:
        """
        Convert distance into a 'closeness' score.
        0km -> 1.0 (best), >= max_distance -> 0.0
        """
        d = clamp(distance_km, 0.0, max_distance_km)
        return 1.0 - (d / max_distance_km)
