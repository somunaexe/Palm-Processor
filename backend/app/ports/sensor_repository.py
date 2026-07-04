from abc import ABC, abstractmethod
from app.domain.models import EnrichedSensorEvent


class SensorRepository(ABC):

    @abstractmethod
    def save(self, event: EnrichedSensorEvent):
        pass

    @abstractmethod
    def get_latest(self, limit: int):
        pass

    @abstractmethod
    def get_machine_history(self, machine_id: str):
        pass