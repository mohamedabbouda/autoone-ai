from typing import List
from app.data.mock_services import MOCK_SERVICES
from app.models.service_model import ServiceModel
from app.data.service_source import ServiceSource

class MockServiceSource(ServiceSource):

    def load_services(self) -> List[ServiceModel]:
        return MOCK_SERVICES
