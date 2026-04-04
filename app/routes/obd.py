from fastapi import APIRouter, HTTPException
from app.models.obd_event_model import DtcEventModel
from app.services.obd_event_store import ObdEventStore

router = APIRouter()
store = ObdEventStore()


@router.post("/obd/dtc")
async def ingest_dtc_event(event: DtcEventModel):
    try:
        store.save_dtc_event(event)
        return {"ok": True, "message": "DTC event stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))