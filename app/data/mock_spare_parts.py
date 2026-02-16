# app/data/mock_spare_parts.py
from app.models.spare_part_model import SparePartModel

MOCK_SPARE_PARTS = [
    SparePartModel(
        id=1,
        name="Brake Pads Front",
        description="Ceramic brake pads for BMW E90",
        brand="Bosch",
        car_make="BMW",
        car_model="E90",
        category="brakes",
        price=79.99
    ),
    SparePartModel(
        id=2,
        name="Oil Filter",
        description="Oil filter compatible with VW Golf",
        brand="Mann",
        car_make="VW",
        car_model="Golf",
        category="engine",
        price=14.50
    ),
]


