from datetime import datetime

class AvailabilityChecker:

    @staticmethod
    def is_open_now(service, distance_km):
        now = datetime.now().time()

        open_time = datetime.strptime(service.open, "%H:%M").time()
        close_time = datetime.strptime(service.close, "%H:%M").time()

        if now < open_time or now > close_time:
            return False, "closed"

        travel_minutes = (distance_km / 30) * 60  
        latest_arrival = (datetime.combine(datetime.today(), close_time)
                          .timestamp() - 20*60)
        arrival_time = datetime.now().timestamp() + travel_minutes*60

        if arrival_time <= latest_arrival:
            return True, "open"
        else:
            return False, "closing_soon"