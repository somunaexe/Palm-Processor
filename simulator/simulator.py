import json
import os
import time
import random
import uuid
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

CONNECTION_STR = os.getenv("EVENTHUB_CONN_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

if not CONNECTION_STR:
    raise ValueError("EVENTHUB_CONN_STR is missing")

if not EVENTHUB_NAME:
    raise ValueError("EVENTHUB_NAME is missing")

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

machines = ["M-100", "M-200", "M-300"]

def generate_sensor_data():
    return {
        # "id": str(uuid.uuid4()),
        "machine_id": random.choice(machines),
        "temperature": round(random.uniform(60, 120), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "pressure": round(random.uniform(20, 80), 2),
        "timestamp": datetime.now().isoformat()
    }

while True:
    event = generate_sensor_data()

    with producer:
        event_batch = producer.create_batch()
        event_batch.add(EventData(json.dumps(event)))
        producer.send_batch(event_batch)

    print("Sent:", event)

    time.sleep(2)