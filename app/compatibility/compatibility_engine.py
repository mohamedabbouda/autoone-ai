from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.models.vehicle_profile import VehicleProfile
from app.models.spare_part_model import SparePartModel


@dataclass
class CompatibilityResult:
    compatible: bool
    confidence: float  # 0..1
    reasons: List[str]


class CompatibilityEngine:
    """
    Rule-based compatibility check v1.
    Later: replace/extend using real fitment tables and richer VIN decoding.
    """

    def check(self, vehicle: VehicleProfile, part: SparePartModel) -> CompatibilityResult:
        reasons: List[str] = []
        score = 0.0
        possible = 0.0

        # --- Rule: make
        if vehicle.make and getattr(part, "car_make", None):
            possible += 1.0
            if part.car_make == vehicle.make:
                score += 1.0
                reasons.append("make_match")
            else:
                reasons.append("make_mismatch")
                return CompatibilityResult(False, 0.0, reasons)

        # --- Rule: model
        if vehicle.model and getattr(part, "car_model", None):
            possible += 1.0
            if part.car_model == vehicle.model:
                score += 1.0
                reasons.append("model_match")
            else:
                reasons.append("model_mismatch")
                return CompatibilityResult(False, 0.0, reasons)

        # --- Rule: year range (only if part has it)
        year_from = getattr(part, "year_from", None)
        year_to = getattr(part, "year_to", None)
        if vehicle.year and (year_from is not None or year_to is not None):
            possible += 1.0
            y1 = int(year_from) if year_from is not None else 1900
            y2 = int(year_to) if year_to is not None else 2100
            if y1 <= int(vehicle.year) <= y2:
                score += 1.0
                reasons.append("year_match")
            else:
                reasons.append("year_mismatch")
                return CompatibilityResult(False, 0.0, reasons)

        # If we couldn't check anything (no metadata), be conservative
        if possible == 0.0:
            return CompatibilityResult(False, 0.2, ["insufficient_metadata"])

        confidence = score / possible
        compatible = confidence >= 0.67  # threshold
        return CompatibilityResult(compatible, confidence, reasons)
