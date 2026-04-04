from typing import Dict
from app.services.dtc_knowledge_base import DTC_KNOWLEDGE


class PredictiveMaintenanceService:

    def predict(self, vin: str, code: str) -> Dict:
        code = code.upper()

        if code not in DTC_KNOWLEDGE:
            return {
                "vin": vin,
                "code": code,
                "issue": "Unknown issue",
                "severity": "low",
                "recommended_action": "Run full diagnostics",
                "urgency_score": 0.3,
            }

        info = DTC_KNOWLEDGE[code]

        return {
            "vin": vin,
            "code": code,
            "issue": info["issue"],
            "severity": info["severity"],
            "recommended_action": info["action"],
            "urgency_score": info["base_score"],
        }