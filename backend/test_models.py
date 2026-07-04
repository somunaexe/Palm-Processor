from datetime import datetime

from app.domain.models import SensorEvent

event = SensorEvent(
    machine_id="M-101",
    temperature=82.4,
    vibration=1.2,
    pressure=53.7,
    timestamp=datetime.now()
)

print(event)