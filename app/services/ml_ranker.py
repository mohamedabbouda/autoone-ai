# from __future__ import annotations

# import pandas as pd
# from typing import Dict, List

# from app.models.service_model import ServiceModel
# from app.services.ml_model_registry import get_model_artifact

# def score_services_ml(
#     services: List[ServiceModel],
#     features_by_id: Dict[int, Dict[str, float]],
#     hour: int,
#     dayofweek: int,
# ) -> Dict[int, float]:
#     artifact = get_model_artifact()
#     if artifact is None:
#         return {}

#     model = artifact["model"]
#     feature_cols = artifact["feature_cols"]

#     rows = []
#     ids = []

#     for s in services:
#         feats = features_by_id.get(s.id, {})
#         row = {
#             "f_rating_norm": feats.get("rating_norm", 0.0),
#             "f_distance_closeness": feats.get("distance_closeness", 0.0),
#             "f_open_now": feats.get("open_now", 0.0),
#             "position": getattr(s, "position", 0),  # optional; not used for scoring candidates
#             "hour": hour,
#             "dayofweek": dayofweek,
#         }
#         rows.append(row)
#         ids.append(s.id)

#     X = pd.DataFrame(rows)[feature_cols].fillna(0.0)
#     proba = model.predict_proba(X)[:, 1]

#     return {sid: float(p) for sid, p in zip(ids, proba)}



from __future__ import annotations

import pandas as pd
from typing import Dict, List

from app.models.service_model import ServiceModel
from app.services.ml_model_registry import get_model_artifact


def score_services_ml(
    services: List[ServiceModel],
    features_by_id: Dict[int, Dict[str, float]],
    hour: int,
    dayofweek: int,
) -> Dict[int, float]:
    artifact = get_model_artifact()
    if artifact is None:
        return {}  # ✅ no model -> fallback

    try:
        model = artifact["model"]
        feature_cols = artifact["feature_cols"]

        rows = []
        ids = []

        for s in services:
            feats = features_by_id.get(s.id, {})
            row = {
                "f_rating_norm": feats.get("rating_norm", 0.0),
                "f_distance_closeness": feats.get("distance_closeness", 0.0),
                "f_open_now": feats.get("open_now", 0.0),
                "position": 0,       # don't use UI position as a feature here
                "hour": hour,
                "dayofweek": dayofweek,
            }
            rows.append(row)
            ids.append(s.id)

        X = pd.DataFrame(rows)[feature_cols].fillna(0.0)
        proba = model.predict_proba(X)[:, 1]

        return {sid: float(p) for sid, p in zip(ids, proba)}

    except Exception:
        return {}  # ✅ any inference error -> fallback