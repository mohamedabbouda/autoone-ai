from app.compatibility.compatibility_engine import CompatibilityEngine
# import uuid
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, validator

# from app.vin.vin_decoder import MockVinDecoder, is_valid_vin
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.data.mock_spare_parts import MOCK_SPARE_PARTS
from app.search.search_engine import SparePartSearchEngine
from app.services.parts_event_logger import PartsEventLogger
from app.search.filters import apply_filters, paginate
from app.vin.vin_decoder import MockVinDecoder, is_valid_vin

from app.models.vehicle_profile import VehicleProfile

router = APIRouter()

compat_engine = CompatibilityEngine()
vin_decoder = MockVinDecoder()


class CompatibilityRequest(BaseModel):
    vin: str
    part_id: int


@router.post("/spare-parts/compatibility")
async def spare_parts_compatibility(req: CompatibilityRequest):
    try:
        vin = req.vin.strip().upper()
        if not is_valid_vin(vin):
            raise HTTPException(status_code=400, detail="Invalid VIN format (17 chars, no I/O/Q).")

        vehicle = vin_decoder.decode(vin)

        # find part in your catalog (mock for now)
        part = next((p for p in MOCK_SPARE_PARTS if p.id == req.part_id), None)
        if not part:
            raise HTTPException(status_code=404, detail="Part not found")

        result = compat_engine.check(vehicle, part)

        return {
            "vin": vin,
            "vehicle": vehicle.model_dump(),
            "part_id": req.part_id,
            "compatible": result.compatible,
            "confidence": result.confidence,
            "reasons": result.reasons,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
