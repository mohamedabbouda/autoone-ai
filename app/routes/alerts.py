from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.services.predictive_maintenance import PredictiveMaintenanceService
from app.services.alert_service import AlertService

router = APIRouter()
predict_service = PredictiveMaintenanceService()
alert_service = AlertService()


class AlertRequest(BaseModel):
    vin: str
    code: str
    user_id: Optional[str] = None


@router.post("/alerts/evaluate")
async def evaluate_alert(req: AlertRequest):
    try:
        prediction = predict_service.predict(req.vin, req.code)

        alert = alert_service.create_from_prediction(
            vin=req.vin,
            issue=prediction["issue"],
            severity=prediction["severity"],
            urgency_score=prediction["urgency_score"],
            user_id=req.user_id,
        )

        return {
            "prediction": prediction,
            "alert": alert.model_dump() if alert else None,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_alerts(vin: Optional[str] = Query(None), user_id: Optional[str] = Query(None)):
    try:
        alerts = alert_service.list_alerts(vin=vin, user_id=user_id)
        return {"alerts": [a.model_dump() for a in alerts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))