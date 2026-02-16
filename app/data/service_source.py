from abc import ABC, abstractmethod
from typing import List
from app.models.service_model import ServiceModel

class ServiceSource(ABC):

    @abstractmethod
    def load_services(self) -> List[ServiceModel]:
        """Return a list of ServiceModel objects"""
        pass
