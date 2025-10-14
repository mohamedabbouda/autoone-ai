import math
from datetime import datetime

# Mock data with opening/closing times (24h format)
SERVICES = [
    {"name": "CleanCar Wash", "lat": 52.5205, "lng": 13.4095, "rating": 4.5, "type": "car_wash", "open": "08:00", "close": "20:00"},
    {"name": "Speedy Wash", "lat": 52.5170, "lng": 13.4000, "rating": 4.2, "type": "car_wash", "open": "09:00", "close": "18:00"},
    {"name": "Budget Wash", "lat": 52.5300, "lng": 13.4100, "rating": 3.8, "type": "car_wash", "open": "07:00", "close": "22:00"},
    {"name": "Berlin Auto Repair", "lat": 52.5190, "lng": 13.4060, "rating": 4.7, "type": "maintenance", "open": "08:00", "close": "17:00"}
]

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance (km) between two lat/lng points"""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def is_open_now(service, distance_km):
    """Check if service is open and reachable 20 min before closing"""
    now = datetime.now().time()

    open_time = datetime.strptime(service["open"], "%H:%M").time()
    close_time = datetime.strptime(service["close"], "%H:%M").time()

    if now < open_time or now > close_time:
        return False, "closed"

    # Estimate travel time
    travel_minutes = (distance_km / 30) * 60  # avg 30 km/h
    latest_arrival = (datetime.combine(datetime.today(), close_time)
                      .timestamp() - 20*60)  # 20 min before close
    arrival_time = datetime.now().timestamp() + travel_minutes*60

    if arrival_time <= latest_arrival:
        return True, "open"
    else:
        return False, "closing_soon"

def get_recommendations(lat: float, lng: float, service_type: str):
    """Return recommended services considering distance, rating, and open status"""
    filtered = [s.copy() for s in SERVICES if s["type"] == service_type]

    for s in filtered:
        s["distance_km"] = round(haversine(lat, lng, s["lat"], s["lng"]), 2)
        open_status, status_text = is_open_now(s, s["distance_km"])
        s["status"] = status_text
        s["is_available"] = open_status

        # Score: balance rating vs distance
        weight_rating = 2.0
        weight_distance = 1.0
        s["score"] = (s["rating"] * weight_rating) - (s["distance_km"] * weight_distance)

    # Sort by:
    # 1. Availability (open first)
    # 2. Combined score (higher = better)
    filtered.sort(key=lambda x: (not x["is_available"], -x["score"]))

    return filtered[:3]
