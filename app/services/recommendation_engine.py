
# app/services/recommendation_engine.py
from __future__ import annotations

from app.features.feature_builder import FeatureBuilder
from app.features.feature_config import FeatureConfig
from app.models.service_model import ServiceModel
from app.services.distance_calculator import DistanceCalculator
from app.services.availability_checker import AvailabilityChecker

class RecommendationEngine:
    def __init__(self, services: list[ServiceModel], config: FeatureConfig | None = None):
        self.services = services
        self.config = config or FeatureConfig()
        self.feature_builder = FeatureBuilder(self.config)

    def recommend_with_features(
        self, user_lat: float, user_lng: float, service_type: str
    ) -> tuple[list[ServiceModel], dict[int, dict[str, float]]]:

        filtered = [s for s in self.services if s.type == service_type]
        feature_map: dict[int, dict[str, float]] = {}

        for s in filtered:
            s.distance_km = round(
                DistanceCalculator.haversine(user_lat, user_lng, s.lat, s.lng), 2
            )

            is_open, status = AvailabilityChecker.is_open_now(s, s.distance_km)
            s.is_available = is_open
            s.status = status

            feats = self.feature_builder.build(s)
            feature_map[s.id] = feats

            s.score = (
                feats["rating_norm"] * self.config.weight_rating
                + feats["distance_closeness"] * self.config.weight_distance
                + feats["open_now"] * self.config.weight_open_now
            )

        filtered.sort(key=lambda x: (not x.is_available, -(x.score or 0.0)))
        top = filtered[: self.config.max_results]
        return top, feature_map

    # keep old method for compatibility
    def recommend(self, user_lat: float, user_lng: float, service_type: str) -> list[ServiceModel]:
        top, _ = self.recommend_with_features(user_lat, user_lng, service_type)
        return top












# import math
# from datetime import datetime

# # Mock data with opening/closing times (24h format)
# SERVICES = [
#     {"name": "CleanCar Wash", "lat": 52.5205, "lng": 13.4095, "rating": 4.5, "type": "car_wash", "open": "08:00", "close": "20:00"},
#     {"name": "Speedy Wash", "lat": 52.5170, "lng": 13.4000, "rating": 4.2, "type": "car_wash", "open": "09:00", "close": "18:00"},
#     {"name": "Budget Wash", "lat": 52.5300, "lng": 13.4100, "rating": 3.8, "type": "car_wash", "open": "07:00", "close": "22:00"},
#     {"name": "Berlin Auto Repair", "lat": 52.5190, "lng": 13.4060, "rating": 4.7, "type": "maintenance", "open": "08:00", "close": "17:00"}
# ]

# def haversine(lat1, lon1, lat2, lon2):
#     """Calculate distance (km) between two lat/lng points"""
#     R = 6371
#     phi1, phi2 = math.radians(lat1), math.radians(lat2)
#     dphi = math.radians(lat2 - lat1)
#     dlambda = math.radians(lon2 - lon1)

#     a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#     return R * c

# def is_open_now(service, distance_km):
#     """Check if service is open and reachable 20 min before closing"""
#     now = datetime.now().time()

#     open_time = datetime.strptime(service["open"], "%H:%M").time()
#     close_time = datetime.strptime(service["close"], "%H:%M").time()

#     if now < open_time or now > close_time:
#         return False, "closed"

#     # Estimate travel time
#     travel_minutes = (distance_km / 30) * 60  # avg 30 km/h
#     latest_arrival = (datetime.combine(datetime.today(), close_time)
#                       .timestamp() - 20*60)  # 20 min before close
#     arrival_time = datetime.now().timestamp() + travel_minutes*60

#     if arrival_time <= latest_arrival:
#         return True, "open"
#     else:
#         return False, "closing_soon"

# def get_recommendations(lat: float, lng: float, service_type: str):
#     """Return recommended services considering distance, rating, and open status"""
#     filtered = [s.copy() for s in SERVICES if s["type"] == service_type]

#     for s in filtered:
#         s["distance_km"] = round(haversine(lat, lng, s["lat"], s["lng"]), 2)
#         open_status, status_text = is_open_now(s, s["distance_km"])
#         s["status"] = status_text
#         s["is_available"] = open_status

#         # Score: balance rating vs distance
#         weight_rating = 2.0
#         weight_distance = 1.0
#         s["score"] = (s["rating"] * weight_rating) - (s["distance_km"] * weight_distance)

#     # Sort by:
#     # 1. Availability (open first)
#     # 2. Combined score (higher = better)
#     filtered.sort(key=lambda x: (not x["is_available"], -x["score"]))

#     return filtered[:3]



# from app.models.service_model import ServiceModel
# from app.services.distance_calculator import DistanceCalculator
# from app.services.availability_checker import AvailabilityChecker
# from app.services.recommendation_config import RecommendationConfig

# class RecommendationEngine:

#     def __init__(self, service_source):
#         self.service_source = service_source


#     def recommend(self, user_lat: float, user_lng: float, service_type: str):
#         services = self.service_source.load_services()


#         filtered = [s for s in services if s.type == service_type]

        

#         for s in filtered:
#             s.distance_km = round(
#                 DistanceCalculator.haversine(user_lat, user_lng, s.lat, s.lng), 2
#             )
#             is_open, status = AvailabilityChecker.is_open_now(s, s.distance_km)
#             s.is_available = is_open
#             s.status = status

#             # scoring
#             s.score = (s.rating * 2.0) - (s.distance_km * 1.0)

#         # sort open services first, higher score first
#         filtered.sort(key=lambda x: (not x.is_available, -s.score))

#         return filtered[:3]











# from app.models.service_model import ServiceModel
# from app.services.distance_calculator import DistanceCalculator
# from app.services.availability_checker import AvailabilityChecker
# from app.services.recommendation_config import RecommendationConfig

# class RecommendationEngine:

#     def __init__(
#         self,
#         services: list[ServiceModel],
#         config: RecommendationConfig = RecommendationConfig()
#     ):
#         self.services = services
#         self.config = config

#     def recommend(self, user_lat: float, user_lng: float, service_type: str):

#         # 1. Filter by service type
#         filtered = [s for s in self.services if s.type == service_type]

#         for s in filtered:
#             # 2. Distance
#             s.distance_km = round(
#                 DistanceCalculator.haversine(
#                     user_lat, user_lng, s.lat, s.lng
#                 ),
#                 2
#             )

#             # 3. Availability
#             s.is_available, s.status = AvailabilityChecker.is_open_now(
#                 s, s.distance_km
#             )

#             # 4. Scoring (config-driven)
#             s.score = (
#                 s.rating * self.config.rating_weight
#                 - s.distance_km * self.config.distance_weight
#             )

#         # 5. Sorting
#         filtered.sort(
#             key=lambda x: (not x.is_available, -x.score)
#         )

#         return filtered[: self.config.max_results]















