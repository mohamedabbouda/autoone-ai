# app/data/mock_services.py

from app.models.service_model import ServiceModel

MOCK_SERVICES: list[ServiceModel] = [
    ServiceModel(
        id=1,
        name="CleanCar Wash",
        lat=52.5205,
        lng=13.4095,
        rating=4.5,
        type="car_wash",
        open="08:00",
        close="20:00",
    ),
    ServiceModel(
        id=2,
        name="Speedy Wash",
        lat=52.5170,
        lng=13.4000,
        rating=4.2,
        type="car_wash",
        open="09:00",
        close="18:00",
    ),
    ServiceModel(
        id=3,
        name="Budget Wash",
        lat=52.5300,
        lng=13.4100,
        rating=3.8,
        type="car_wash",
        open="07:00",
        close="22:00",
    ),
    ServiceModel(
        id=4,
        name="Berlin Auto Repair",
        lat=52.5190,
        lng=13.4060,
        rating=4.7,
        type="maintenance",
        open="08:00",
        close="17:00",
    ),
]
