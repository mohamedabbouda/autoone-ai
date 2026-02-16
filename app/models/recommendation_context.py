

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class RecommendationContext:
    request_id: str
    service_type: str
    user_lat: float
    user_lng: float
    request_time: datetime
    user_id: Optional[str] = None
    ranking_mode: Optional[str] = None  # ✅ NEW ("rules", "ml", "rules_fallback")

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "service_type": self.service_type,
            "user_lat": self.user_lat,
            "user_lng": self.user_lng,
            "request_time": self.request_time.isoformat(),
            "user_id": self.user_id,
            "ranking_mode": self.ranking_mode,  # ✅ NEW
        }