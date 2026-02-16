# from pydantic import BaseModel
# from typing import Optional

# class ServiceModel(BaseModel):
#     id: Optional[int] = None
#     name: str
#     lat: float
#     lng: float
#     rating: float
#     type: str
#     open: str
#     close: str
    
from pydantic import BaseModel
from typing import Optional

class ServiceModel(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    rating: float
    type: str
    open: str
    close: str


    # Computed fields (we add them during recommendation)
    distance_km: Optional[float] = None
    is_available: Optional[bool] = None
    status: Optional[str] = None
    score: Optional[float] = None

    class Config:
        extra = "allow"
        
    