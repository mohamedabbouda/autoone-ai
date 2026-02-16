
# app/models/spare_part_model.py
from pydantic import BaseModel
from typing import Optional

class SparePartModel(BaseModel):
    id: int
    name: str
    description: str
    brand: str
    car_make: Optional[str]
    car_model: Optional[str]
    category: str
    price: float
    score: Optional[float] = None

    class Config:
        extra = "allow"

        


