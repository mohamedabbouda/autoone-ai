


# # app/routes/recommend.py
# import uuid
# from datetime import datetime
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional

# from app.data.mock_service_source import MockServiceSource
# from app.services.recommendation_engine import RecommendationEngine
# from app.features.feature_config import FeatureConfig
# from app.models.recommendation_context import RecommendationContext
# from app.services.recommendation_event_logger import RecommendationEventLogger
# from datetime import datetime
# from app.services.ml_ranker import score_services_ml


# router = APIRouter()
# logger = RecommendationEventLogger()

# class RecommendRequest(BaseModel):
#     service: str
#     lat: Optional[float] = None
#     lng: Optional[float] = None
#     user_id: Optional[str] = None

# @router.post("/recommend")
# async def recommend(req: RecommendRequest):
#     try:
#         lat = req.lat if req.lat is not None else 52.5200
#         lng = req.lng if req.lng is not None else 13.4050

#         source = MockServiceSource()
#         services = source.load_services()

#         engine = RecommendationEngine(services=services, config=FeatureConfig())

#         request_id = str(uuid.uuid4())  # ✅ NEW

#         context = RecommendationContext(
#             request_id=request_id,       # ✅ NEW
#             service_type=req.service,
#             user_lat=lat,
#             user_lng=lng,
#             request_time=datetime.utcnow(),
#             user_id=req.user_id,
#         )

#         results, feats = engine.recommend_with_features(lat, lng, req.service)

#         logger.log_impression(context, results, feats)

#         if not results:
#             return {"request_id": request_id, "message": f"No services found for type '{req.service}'"}

#         # ✅ Return request_id so client can send it back on click
#         return {"request_id": request_id, "recommendations": results}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @router.post("/recommend_ml")
# async def recommend_ml(req: RecommendRequest):
#     try:
#         lat = req.lat if req.lat is not None else 52.5200
#         lng = req.lng if req.lng is not None else 13.4050

#         source = MockServiceSource()
#         services = source.load_services()

#         engine = RecommendationEngine(services=services, config=FeatureConfig())

#         request_id = str(uuid.uuid4())
#         now = datetime.utcnow()

#         context = RecommendationContext(
#             request_id=request_id,
#             service_type=req.service.value if hasattr(req.service, "value") else req.service,
#             user_lat=lat,
#             user_lng=lng,
#             request_time=now,
#             user_id=req.user_id,
#         )

#         results, feats = engine.recommend_with_features(lat, lng, context.service_type)

#         # ML scores
#         ml_scores = score_services_ml(
#             services=results,
#             features_by_id=feats,
#             hour=now.hour,
#             dayofweek=now.weekday(),
#         )

#         # Attach ML score and sort by it
#         for s in results:
#             s.ml_score = ml_scores.get(s.id, 0.0)

#         results.sort(key=lambda x: (not x.is_available, -(getattr(x, "ml_score", 0.0))))

#         logger.log_impression(context, results, feats)

#         if not results:
#             return {"request_id": request_id, "message": f"No services found for type '{context.service_type}'"}

#         return {"request_id": request_id, "recommendations": results}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # app/routes/recommend.py (add below)
# class ClickRequest(BaseModel):
#     request_id: str          # ✅ NEW (required)
#     service: str
#     lat: float
#     lng: float
#     service_id: int
#     position: Optional[int] = None
#     user_id: Optional[str] = None


# @router.post("/recommend/click")
# async def recommend_click(req: ClickRequest):
#     try:
#         context = RecommendationContext(
#             request_id=req.request_id,   # ✅ NEW
#             service_type=req.service,
#             user_lat=req.lat,
#             user_lng=req.lng,
#             request_time=datetime.utcnow(),
#             user_id=req.user_id,
#         )
#         logger.log_click(context, req.service_id, req.position)
#         return {"ok": True}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))












# app/routes/recommend.py
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data.mock_service_source import MockServiceSource
from app.features.feature_config import FeatureConfig
from app.models.recommendation_context import RecommendationContext
from app.services.ml_ranker import score_services_ml
from app.services.recommendation_engine import RecommendationEngine
from app.services.recommendation_event_logger import RecommendationEventLogger

router = APIRouter()
logger = RecommendationEventLogger()


class RecommendRequest(BaseModel):
    service: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    user_id: Optional[str] = None


@router.post("/recommend")
async def recommend(req: RecommendRequest):
    try:
        lat = req.lat if req.lat is not None else 52.5200
        lng = req.lng if req.lng is not None else 13.4050

        source = MockServiceSource()
        services = source.load_services()

        engine = RecommendationEngine(services=services, config=FeatureConfig())

        request_id = str(uuid.uuid4())
        now = datetime.utcnow()

        context = RecommendationContext(
            request_id=request_id,
            service_type=req.service,
            user_lat=lat,
            user_lng=lng,
            request_time=now,
            user_id=req.user_id,
            ranking_mode="rules",   # ✅ NEW

        )

        results, feats = engine.recommend_with_features(lat, lng, req.service)

        logger.log_impression(context, results, feats)

        if not results:
            return {"request_id": request_id, "message": f"No services found for type '{req.service}'"}

        return {"request_id": request_id, "recommendations": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend_ml")
async def recommend_ml(req: RecommendRequest):
    try:
        lat = req.lat if req.lat is not None else 52.5200
        lng = req.lng if req.lng is not None else 13.4050

        source = MockServiceSource()
        services = source.load_services()

        engine = RecommendationEngine(services=services, config=FeatureConfig())

        request_id = str(uuid.uuid4())
        now = datetime.utcnow()

        context = RecommendationContext(
            request_id=request_id,
            service_type=req.service,  # ✅ service is str
            user_lat=lat,
            user_lng=lng,
            request_time=now,
            user_id=req.user_id,

        )

        # Get candidates + features
        results, feats = engine.recommend_with_features(lat, lng, context.service_type)

        # ML scores for the returned candidates
        ml_scores = score_services_ml(
            services=results,
            features_by_id=feats,
            hour=now.hour,
            dayofweek=now.weekday(),
        )

        # Attach ml_score and sort
        for s in results:
            s.ml_score = ml_scores.get(s.id, 0.0)

        results.sort(key=lambda x: (not x.is_available, -(getattr(x, "ml_score", 0.0))))

        logger.log_impression(context, results, feats)

        if not results:
            return {"request_id": request_id, "message": f"No services found for type '{context.service_type}'"}

        return {"request_id": request_id, "recommendations": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ClickRequest(BaseModel):
    request_id: str
    service: str
    lat: float
    lng: float
    service_id: int
    position: Optional[int] = None
    user_id: Optional[str] = None


@router.post("/recommend/click")
async def recommend_click(req: ClickRequest):
    try:
        now = datetime.utcnow()
        context = RecommendationContext(
            request_id=req.request_id,
            service_type=req.service,
            user_lat=req.lat,
            user_lng=req.lng,
            request_time=now,
            user_id=req.user_id,
        )
        logger.log_click(context, req.service_id, req.position)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
