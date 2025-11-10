from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.recommend_service import get_recommendations
from typing import Optional


router = APIRouter()

class RecommendRequest(BaseModel):
    service: str   # required
    lat: Optional[float] = None
    lng: Optional[float] = None  # e.g. "car_wash" or "maintenance"

@router.post("/recommend")
async def recommend(req: RecommendRequest):
    try:
        # Default location (Berlin center) if no coords provided
        lat = req.lat if req.lat is not None else 52.5200
        lng = req.lng if req.lng is not None else 13.4050

        results = get_recommendations(lat, lng, req.service)

        if not results:
            return {"message": f"No services found for type '{req.service}'"}

        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
