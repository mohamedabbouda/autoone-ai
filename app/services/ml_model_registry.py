from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import joblib

MODEL_PATH = Path("models/reco_lr.pkl")

_cached: Optional[Dict[str, Any]] = None

def get_model_artifact() -> Optional[Dict[str, Any]]:
    global _cached
    if _cached is not None:
        return _cached
    if not MODEL_PATH.exists():
        return None
    _cached = joblib.load(MODEL_PATH)
    return _cached
