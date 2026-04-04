from typing import List, Optional

from app.models.offer_model import OfferModel


class OfferService:
    def generate_offers(
        self,
        vin: str,
        issue: str,
        recommended_action: str,
        severity: str,
        user_id: Optional[str] = None,
    ) -> List[OfferModel]:
        offers: List[OfferModel] = []

        issue_lower = issue.lower()

        if "coolant" in issue_lower or "thermostat" in issue_lower:
            offers.append(
                OfferModel(
                    vin=vin,
                    user_id=user_id,
                    offer_type="service_offer",
                    title="Cooling System Check",
                    reason="Coolant temperature issue detected",
                    recommended_action=recommended_action,
                    priority=1,
                )
            )

        elif "misfire" in issue_lower or "cylinder" in issue_lower:
            offers.append(
                OfferModel(
                    vin=vin,
                    user_id=user_id,
                    offer_type="service_offer",
                    title="Ignition System Inspection",
                    reason="Misfire-related issue detected",
                    recommended_action=recommended_action,
                    priority=1,
                )
            )

        elif "lean" in issue_lower or "fuel" in issue_lower:
            offers.append(
                OfferModel(
                    vin=vin,
                    user_id=user_id,
                    offer_type="service_offer",
                    title="Fuel and Air Intake Check",
                    reason="Fuel/air mixture issue detected",
                    recommended_action=recommended_action,
                    priority=2,
                )
            )

        elif "catalyst" in issue_lower or "catalytic" in issue_lower:
            offers.append(
                OfferModel(
                    vin=vin,
                    user_id=user_id,
                    offer_type="service_offer",
                    title="Exhaust System Inspection",
                    reason="Catalyst efficiency issue detected",
                    recommended_action=recommended_action,
                    priority=2,
                )
            )

        else:
            offers.append(
                OfferModel(
                    vin=vin,
                    user_id=user_id,
                    offer_type="service_offer",
                    title="General Diagnostic Check",
                    reason="A vehicle issue was detected",
                    recommended_action=recommended_action,
                    priority=3,
                )
            )

        return offers