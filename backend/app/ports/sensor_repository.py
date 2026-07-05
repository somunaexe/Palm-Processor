from abc import ABC, abstractmethod
from app.domain.models import EnrichedSensorEvent

class SensorRepository(ABC):
    """Contract for storing and retrieving sensor events."""

    @abstractmethod
    def save(self, event: EnrichedSensorEvent) -> None:
        """Persist a sensor event."""
        pass

    @abstractmethod
    def save_many(self, events: list[EnrichedSensorEvent]) -> None:
        """Persist multiple sensor events."""
        pass

    @abstractmethod
    def get_latest(self, limit: int = 100) -> list[EnrichedSensorEvent]:
        """Return the newest events."""
        pass

    @abstractmethod
    def get_machine_history(
        self,
        machine_id: str,
    ) -> list[EnrichedSensorEvent]:
        """Return history for one machine."""
        pass