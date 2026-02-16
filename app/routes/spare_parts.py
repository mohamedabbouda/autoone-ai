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

logger = PartsEventLogger()
engine = SparePartSearchEngine(MOCK_SPARE_PARTS)
vin_decoder = MockVinDecoder()



class SearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    # limit: int = 10

    # ✅ C2 pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)

    # ✅ C2 filters
    category: Optional[str] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    vin: Optional[str] = None
    in_stock: Optional[bool] = None



@router.post("/spare-parts/search")
async def search_spare_parts(req: SearchRequest):
    try:
        request_id = str(uuid.uuid4())
        # results = engine.search(req.query, limit=req.limit)
        candidates = engine.search(req.query)  # ✅ remove limit here



        # 2) filters
        filtered = apply_filters(
            candidates,
            category=req.category,
            min_price=req.min_price,
            max_price=req.max_price,
            vin=req.vin,
            in_stock=req.in_stock,
        )

        # 3) pagination
        page_items, total, total_pages = paginate(
            filtered,
            page=req.page,
            page_size=req.page_size,
        )

        # log impression (log only page items OR all filtered—your choice)
        # ✅ recommended: log only returned items (what user actually saw)
        logger.log_impression(
            request_id=request_id,
            user_id=req.user_id,
            query=req.query,
            results=page_items,
        )

        return {
            "request_id": request_id,
            "query": req.query,
            "filters": {
                "category": req.category,
                "min_price": req.min_price,
                "max_price": req.max_price,
                "vin": req.vin,
                "in_stock": req.in_stock,
            },
            "page": req.page,
            "page_size": req.page_size,
            "total": total,
            "total_pages": total_pages,
            "results": page_items,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









class ClickRequest(BaseModel):
    request_id: str
    part_id: int
    position: Optional[int] = None
    user_id: Optional[str] = None

@router.post("/spare-parts/click")
async def spare_parts_click(req: ClickRequest):
    try:
        logger.log_click(
            request_id=req.request_id,
            user_id=req.user_id,
            part_id=req.part_id,
            position=req.position,
        )
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    








class VinSearchRequest(BaseModel):
    vin: str
    query: str = ""
    user_id: Optional[str] = None

    # reuse C2 pagination + filters
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)

    category: Optional[str] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    in_stock: Optional[bool] = None


@router.post("/spare-parts/search/vin")
async def search_spare_parts_by_vin(req: VinSearchRequest):
    try:
        request_id = str(uuid.uuid4())
        vin = req.vin.strip().upper()

        # ✅ VIN format validation
        if not is_valid_vin(vin):
            raise HTTPException(status_code=400, detail="Invalid VIN format (17 chars, no I/O/Q).")

        # ✅ decode VIN to vehicle profile (mock for now)
        vehicle: VehicleProfile = vin_decoder.decode(vin)

        # 1) keyword search
        candidates = engine.search(req.query or "")

        # 2) vehicle-based filtering (only if your parts have car_make/car_model)
        filtered_vehicle = candidates

        if vehicle.make:
            filtered_vehicle = [
                p for p in filtered_vehicle
                if (getattr(p, "car_make", None) is None) or (p.car_make == vehicle.make)
            ]

        if vehicle.model:
            filtered_vehicle = [
                p for p in filtered_vehicle
                if (getattr(p, "car_model", None) is None) or (p.car_model == vehicle.model)
            ]

        # 3) apply existing filters (category/price/stock)
        filtered = apply_filters(
            filtered_vehicle,
            category=req.category,
            min_price=req.min_price,
            max_price=req.max_price,
            vin=None,  # VIN here is vehicle VIN, not part VIN
            in_stock=req.in_stock,
        )

        # 4) paginate (with clamped page)
        page_items, total, total_pages, page = paginate(
            filtered,
            page=req.page,
            page_size=req.page_size,
        )

        # ✅ log impression
        logger.log_impression(
            request_id=request_id,
            user_id=req.user_id,
            query=f"[VIN:{vin}] {req.query}".strip(),
            results=page_items,
        )

        return {
            "request_id": request_id,
            "vin": vin,
            "vehicle": vehicle.model_dump(),
            "filters": {
                "category": req.category,
                "min_price": req.min_price,
                "max_price": req.max_price,
                "in_stock": req.in_stock,
            },
            "page": page,
            "page_size": req.page_size,
            "total": total,
            "total_pages": total_pages,
            "results": page_items,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






