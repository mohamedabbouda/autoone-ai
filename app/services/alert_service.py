from datetime import datetime
from typing import List, Optional

from app.models.alert_model import AlertModel
from app.services.alert_store import AlertStore


class AlertService:
    def __init__(self):
        self.store = AlertStore()

    def create_from_prediction(
        self,
        vin: str,
        issue: str,
        severity: str,
        urgency_score: float,
        user_id: Optional[str] = None,
    ) -> Optional[AlertModel]:
        """
        Create an alert only if urgency is high enough.
        """
        if urgency_score < 0.7:
            return None

        message = f"{issue}. Service is recommended soon."

        alert = AlertModel(
            vin=vin,
            user_id=user_id,
            alert_type="maintenance_warning",
            severity=severity,
            message=message,
            created_at=datetime.utcnow(),
            acknowledged=False,
        )

        self.store.save_alert(alert)
        return alert

    def list_alerts(self, vin: Optional[str] = None, user_id: Optional[str] = None) -> List[AlertModel]:
        alerts = self.store.load_alerts()

        if vin:
            alerts = [a for a in alerts if a.vin == vin]

        if user_id:
            alerts = [a for a in alerts if a.user_id == user_id]

        return alerts