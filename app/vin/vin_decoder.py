

from __future__ import annotations
import re
from abc import ABC, abstractmethod
from app.models.vehicle_profile import VehicleProfile

VIN_RE = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")  # no I,O,Q

def is_valid_vin(vin: str) -> bool:
    return bool(VIN_RE.match(vin.strip().upper()))

class VinDecoder(ABC):
    @abstractmethod
    def decode(self, vin: str) -> VehicleProfile:
        pass

class MockVinDecoder(VinDecoder):
    def decode(self, vin: str) -> VehicleProfile:
        v = vin.strip().upper()

        # Simple examples — extend later
        if v.startswith("WVW"):   # VW
            return VehicleProfile(vin=v, make="VW", model="Golf", year=2018)
        if v.startswith("WBA"):   # BMW
            return VehicleProfile(vin=v, make="BMW", model="3 Series", year=2020)

        return VehicleProfile(vin=v)  # unknown -> still valid format
