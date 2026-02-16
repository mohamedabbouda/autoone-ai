# app/services/recommendation_event_logger.py
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models.recommendation_context import RecommendationContext
from app.models.service_model import ServiceModel

@dataclass
class RecommendedItemLog:
    service_id: int
    score: Optional[float]
    distance_km: Optional[float]
    is_available: Optional[bool]
    status: Optional[str]
    features: Dict[str, float]

class RecommendationEventLogger:
    def __init__(self, logfile: str = "data/reco_events.jsonl"):
        self.path = Path(logfile)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, payload: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def log_impression(
        self,
        context: RecommendationContext,
        recommended: List[ServiceModel],
        features: Dict[int, Dict[str, float]],
    ) -> None:
        payload: Dict[str, Any] = {
            "event_type": "recommendation_impression",
            "timestamp": datetime.utcnow().isoformat(),
            "context": context.to_dict(),  # ✅ FIX
            "recommended": [
                asdict(
                    RecommendedItemLog(
                        service_id=s.id,
                        score=s.score,
                        distance_km=s.distance_km,
                        is_available=s.is_available,
                        status=s.status,
                        features=features.get(s.id, {}),
                    )
                )
                for s in recommended
            ],
        }
        self._write(payload)

    def log_click(
        self,
        context: RecommendationContext,
        service_id: int,
        position: Optional[int] = None,
    ) -> None:
        payload: Dict[str, Any] = {
            "event_type": "recommendation_click",
            "timestamp": datetime.utcnow().isoformat(),
            "context": context.to_dict(),  # ✅ FIX
            "clicked": {"service_id": service_id, "position": position},
        }
        self._write(payload)

