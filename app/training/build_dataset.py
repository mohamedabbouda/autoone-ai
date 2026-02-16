from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


LOG_PATH = Path("data/reco_events.jsonl")
OUT_DIR = Path("data/datasets")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def _round_coord(x: float, decimals: int = 3) -> float:
    return round(float(x), decimals)


def make_session_key(context: Dict[str, Any]) -> str:
    """
    Fallback join key for OLD logs that don't have request_id.
    Not perfect, but works for MVP.
    """
    user_id = context.get("user_id") or "anon"
    service_type = context.get("service_type", "unknown")
    lat = _round_coord(context.get("user_lat", 0.0), 3)
    lng = _round_coord(context.get("user_lng", 0.0), 3)

    rt = context.get("request_time")
    if isinstance(rt, str) and rt:
        t = _parse_iso(rt)
    else:
        t = datetime.utcnow()

    time_bucket = t.strftime("%Y-%m-%dT%H:%M")
    return f"{user_id}|{service_type}|{lat}|{lng}|{time_bucket}"


@dataclass
class ImpressionRow:
    request_id: Optional[str]       # ✅ NEW
    session_key: str
    user_id: str
    service_type: str
    user_lat: float
    user_lng: float
    request_time: datetime
    event_ts: datetime
    service_id: int
    position: int
    score: Optional[float]
    distance_km: Optional[float]
    is_available: Optional[bool]
    status: Optional[str]
    features: Dict[str, float]


@dataclass
class ClickRow:
    request_id: Optional[str]       # ✅ NEW
    session_key: str
    user_id: str
    service_type: str
    user_lat: float
    user_lng: float
    request_time: datetime
    event_ts: datetime
    clicked_service_id: int
    position: Optional[int]


def read_events(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    events: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def split_events(events: List[Dict[str, Any]]) -> Tuple[List[ImpressionRow], List[ClickRow]]:
    impressions: List[ImpressionRow] = []
    clicks: List[ClickRow] = []

    for e in events:
        etype = e.get("event_type")
        event_ts = _parse_iso(e["timestamp"])

        ctx = e.get("context") or {}
        rid = ctx.get("request_id")  # ✅ NEW (may be None for old logs)
        sk = make_session_key(ctx)

        user_id = str(ctx.get("user_id") or "anon")
        service_type = str(ctx.get("service_type") or "unknown")
        user_lat = float(ctx.get("user_lat") or 0.0)
        user_lng = float(ctx.get("user_lng") or 0.0)

        rt_raw = ctx.get("request_time")
        request_time = _parse_iso(rt_raw) if isinstance(rt_raw, str) and rt_raw else datetime.utcnow()

        if etype == "recommendation_impression":
            for pos, item in enumerate(e.get("recommended", [])):
                impressions.append(
                    ImpressionRow(
                        request_id=rid,
                        session_key=sk,
                        user_id=user_id,
                        service_type=service_type,
                        user_lat=user_lat,
                        user_lng=user_lng,
                        request_time=request_time,
                        event_ts=event_ts,
                        service_id=int(item["service_id"]),
                        position=pos,
                        score=item.get("score"),
                        distance_km=item.get("distance_km"),
                        is_available=item.get("is_available"),
                        status=item.get("status"),
                        features=item.get("features") or {},
                    )
                )

        elif etype == "recommendation_click":
            clicked = e.get("clicked") or {}
            clicks.append(
                ClickRow(
                    request_id=rid,
                    session_key=sk,
                    user_id=user_id,
                    service_type=service_type,
                    user_lat=user_lat,
                    user_lng=user_lng,
                    request_time=request_time,
                    event_ts=event_ts,
                    clicked_service_id=int(clicked.get("service_id")),
                    position=clicked.get("position"),
                )
            )

    return impressions, clicks


def build_training_dataframe(impressions: List[ImpressionRow], clicks: List[ClickRow]) -> pd.DataFrame:
    imp_df = pd.DataFrame([vars(x) for x in impressions])
    clk_df = pd.DataFrame([vars(x) for x in clicks])

    if imp_df.empty:
        raise RuntimeError("No impression events found. Call /api/recommend first to generate logs.")

    # If no clicks yet, labels are all 0
    if clk_df.empty:
        imp_df["label_clicked"] = 0
    else:
        # ✅ Prefer request_id join if we have it in BOTH impressions and clicks
        have_request_id = (
            "request_id" in imp_df.columns
            and "request_id" in clk_df.columns
            and imp_df["request_id"].notna().any()
            and clk_df["request_id"].notna().any()
        )

        if have_request_id:
            clk_pairs = set(
                zip(
                    clk_df["request_id"].astype(str),
                    clk_df["clicked_service_id"].astype(int),
                )
            )

            imp_df["label_clicked"] = [
                1 if (str(rid), int(sid)) in clk_pairs else 0
                for rid, sid in zip(imp_df["request_id"], imp_df["service_id"])
            ]
        else:
            # fallback heuristic join (old logs)
            clk_pairs = set(
                zip(
                    clk_df["session_key"].astype(str),
                    clk_df["clicked_service_id"].astype(int),
                )
            )

            imp_df["label_clicked"] = [
                1 if (str(sk), int(sid)) in clk_pairs else 0
                for sk, sid in zip(imp_df["session_key"], imp_df["service_id"])
            ]

    # Expand features dict into columns
    feat_df = pd.json_normalize(imp_df["features"]).add_prefix("f_")
    out = pd.concat([imp_df.drop(columns=["features"]), feat_df], axis=1)

    # Type safety
    out["event_ts"] = pd.to_datetime(out["event_ts"])
    out["request_time"] = pd.to_datetime(out["request_time"])

    # Useful derived columns
    out["hour"] = out["request_time"].dt.hour
    out["dayofweek"] = out["request_time"].dt.dayofweek

    # Ensure expected feature columns exist
    expected = ["f_rating_norm", "f_distance_closeness", "f_open_now"]
    for c in expected:
        if c not in out.columns:
            out[c] = 0.0

    return out


def main() -> None:
    events = read_events(LOG_PATH)
    impressions, clicks = split_events(events)

    df = build_training_dataframe(impressions, clicks)

    csv_path = OUT_DIR / "reco_training.csv"
    df.to_csv(csv_path, index=False)

    # Optional parquet
    try:
        pq_path = OUT_DIR / "reco_training.parquet"
        df.to_parquet(pq_path, index=False)
    except Exception:
        pass

    print(f"✅ Built dataset with {len(df)} rows")
    print(f"✅ Wrote: {csv_path}")


if __name__ == "__main__":
    main()
