from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.models.alert_model import AlertModel


class AlertStore:
    def __init__(self, logfile: str = "data/alerts.jsonl"):
        self.path = Path(logfile)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save_alert(self, alert: AlertModel) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(alert.model_dump(mode="json")) + "\n")

    def load_alerts(self) -> List[AlertModel]:
        if not self.path.exists():
            return []

        alerts: List[AlertModel] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                alerts.append(AlertModel(**json.loads(line)))
        return alerts