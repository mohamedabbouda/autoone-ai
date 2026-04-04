from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DtcEventModel(BaseModel):
    vin: str
    user_id: Optional[str] = None
    code: str
    timestamp: datetime