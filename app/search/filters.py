from __future__ import annotations

from math import ceil
from typing import Iterable, Optional, Tuple, List

from app.models.spare_part_model import SparePartModel


def apply_filters(
    parts: Iterable[SparePartModel],
    *,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    vin: Optional[str] = None,
    in_stock: Optional[bool] = None,
) -> List[SparePartModel]:
    out = list(parts)

    if category:
        c = category.strip().lower()
        out = [p for p in out if (p.category or "").strip().lower() == c]

    if min_price is not None:
        out = [p for p in out if p.price >= float(min_price)]

    if max_price is not None:
        out = [p for p in out if p.price <= float(max_price)]

    if vin:
        v = vin.strip().upper()
        out = [p for p in out if (getattr(p, "vin", None) or "").upper() == v]

    if in_stock is not None:
        out = [p for p in out if bool(getattr(p, "in_stock", True)) == bool(in_stock)]

    return out



def paginate(items: List[SparePartModel], *, page: int, page_size: int) -> Tuple[List[SparePartModel], int, int, int]:
    total = len(items)
    total_pages = max(1, ceil(total / page_size))

    page = max(1, min(page, total_pages))  # ✅ clamp
    start = (page - 1) * page_size
    end = start + page_size

    return items[start:end], total, total_pages, page

    