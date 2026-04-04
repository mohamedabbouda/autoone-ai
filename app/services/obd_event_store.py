from __future__ import annotations

import json
from pathlib import Path
from app.models.obd_event_model import DtcEventModel


class ObdEventStore:
    def __init__(self, logfile: str = "data/obd_dtc_events.jsonl"):
        self.path = Path(logfile)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save_dtc_event(self, event: DtcEventModel) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.model_dump(mode="json")) + "\n")