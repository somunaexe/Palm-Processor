import json
import logging
import os
import threading
from fastapi import FastAPI
from azure.eventhub import EventHubConsumerClient
# from app.ml.model import predict_risk
# from app.db.sql import insert_many
# from collections import deque
from app.services.factory import create_sensor_service
from app.adapters.database.database import SessionLocal
from app.domain.models import SensorEvent
from app.api.routes.events import router as events_router

app = FastAPI()
app.include_router(events_router)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CONNECTION_STR = os.getenv("EVENTHUB_CONN_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")
CONSUMER_GROUP = "$Default"

def get_service():
    db = SessionLocal()
    return create_sensor_service(db)

service = get_service()

def on_event(partition_context, event):
    data = json.loads(event.body_as_str())
    logger.info(f"📥 RECEIVED EVENT: {data}")

    sensor_event = SensorEvent(**data)
    enriched = service.process_events(sensor_event)

    logger.info(f"⚙️ PROCESSED EVENT: {enriched}")

    partition_context.update_checkpoint(event)


def start_consumer():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME
    )

    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1"
        )

@app.on_event("startup")
def startup():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()


@app.get("/")
def health():
    return {"status": "running"}


# @app.get("/events")
# def get_events():
#     return events

# @app.get("/machines")
# def a():
#     return

# @app.get("/machines/{machine_id}")
# def a():
#     return

# @app.get("/alerts")
# def a():
#     return

# @app.get("/analytics")
# def a():
#     return