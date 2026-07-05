from app.domain.models import SensorEvent, EnrichedSensorEvent
from app.ports.sensor_repository import SensorRepository
from app.services.prediction_service import PredictionService


class SensorService:
    
    def __init__(self, sensor_repository: SensorRepository, prediction_service: PredictionService,):
        self.sensor_repository = sensor_repository
        self.prediction_service = prediction_service
        self.event_buffer = []
        self.BATCH_SIZE = 50

    def process_event(self, event: SensorEvent) -> EnrichedSensorEvent:
        prediction = self.prediction_service.predict(event)

        enriched = EnrichedSensorEvent(
            machine_id=event.machine_id,
            temperature=event.temperature,
            vibration=event.vibration,
            pressure=event.pressure,
            timestamp=event.timestamp,
            risk_score=prediction.risk_score,
            status=prediction.status,
        )

        self.sensor_repository.save(enriched)

        return enriched
    
    def process_events(self, event: SensorEvent) -> list[EnrichedSensorEvent]:

        enriched_events = []
        self.event_buffer.append(event)
        
        if len(self.event_buffer) > self.BATCH_SIZE:
            for e in self.event_buffer:
                enriched = self.process_event(e)
                enriched_events.append(enriched)

        return enriched_events