from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.recommend_service import get_recommendations

router = APIRouter()

class RecommendRequest(BaseModel):
    lat: float
    lng: float
    service: str   # e.g. "car_wash" or "maintenance"

@router.post("/recommend")
async def recommend(req: RecommendRequest):
    try:
        results = get_recommendations(req.lat, req.lng, req.service)
        if not results:
            return {"message": f"No services found for type '{req.service}'"}
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
