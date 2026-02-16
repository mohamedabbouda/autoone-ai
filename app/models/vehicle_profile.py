from pydantic import BaseModel
from typing import Optional

class VehicleProfile(BaseModel):
    vin: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
