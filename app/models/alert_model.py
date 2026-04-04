from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertModel(BaseModel):
    vin: str
    user_id: Optional[str] = None
    alert_type: str
    severity: str
    message: str
    created_at: datetime
    acknowledged: bool = False