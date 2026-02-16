from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models.spare_part_model import SparePartModel

class PartsEventLogger:
    def __init__(self, logfile: str = "data/parts_events.jsonl"):
        self.path = Path(logfile)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, payload: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def log_impression(
        self,
        request_id: str,
        user_id: Optional[str],
        query: str,
        results: List[SparePartModel],
    ) -> None:
        self._write({
            "event_type": "parts_impression",
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "user_id": user_id,
            "query": query,
            "results": [
                {
                    "part_id": p.id,
                    "score": getattr(p, "score", None),
                    "price": p.price,
                    "brand": p.brand,
                    "category": p.category,
                }
                for p in results
            ],
        })

    def log_click(
        self,
        request_id: str,
        user_id: Optional[str],
        part_id: int,
        position: Optional[int],
    ) -> None:
        self._write({
            "event_type": "parts_click",
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "user_id": user_id,
            "clicked": {
                "part_id": part_id,
                "position": position,
            },
        })



    





