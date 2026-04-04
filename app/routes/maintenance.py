from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.predictive_maintenance import PredictiveMaintenanceService
from app.data.mock_service_source import MockServiceSource
from app.services.recommendation_engine import RecommendationEngine
from app.features.feature_config import FeatureConfig

router = APIRouter()
service = PredictiveMaintenanceService()


class MaintenanceRequest(BaseModel):
    vin: str
    code: str


class MaintenanceRecommendRequest(BaseModel):
    vin: str
    code: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    user_id: Optional[str] = None


@router.post("/maintenance/predict")
async def predict_maintenance(req: MaintenanceRequest):
    try:
        result = service.predict(req.vin, req.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/maintenance/recommend")
async def recommend_maintenance(req: MaintenanceRecommendRequest):
    try:
        # 1) predict issue
        prediction = service.predict(req.vin, req.code)

        # 2) use recommendation engine to recommend maintenance workshops
        lat = req.lat if req.lat is not None else 52.5200
        lng = req.lng if req.lng is not None else 13.4050

        source = MockServiceSource()
        services = source.load_services()

        engine = RecommendationEngine(
            services=services,
            config=FeatureConfig()
        )

        recommendations = engine.recommend(lat, lng, "maintenance")

        return {
            "prediction": prediction,
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))