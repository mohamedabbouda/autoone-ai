from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.predictive_maintenance import PredictiveMaintenanceService
from app.services.offer_service import OfferService

router = APIRouter()
predict_service = PredictiveMaintenanceService()
offer_service = OfferService()


class OfferRequest(BaseModel):
    vin: str
    code: str
    user_id: Optional[str] = None


@router.post("/offers/recommended")
async def get_recommended_offers(req: OfferRequest):
    try:
        prediction = predict_service.predict(req.vin, req.code)

        offers = offer_service.generate_offers(
            vin=req.vin,
            issue=prediction["issue"],
            recommended_action=prediction["recommended_action"],
            severity=prediction["severity"],
            user_id=req.user_id,
        )

        return {
            "prediction": prediction,
            "offers": [o.model_dump() for o in offers]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))