from pydantic import BaseModel
from typing import Optional


class OfferModel(BaseModel):
    vin: str
    user_id: Optional[str] = None
    offer_type: str
    title: str
    reason: str
    recommended_action: str
    priority: int