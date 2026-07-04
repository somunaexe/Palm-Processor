import os
import json
import threading
from fastapi import FastAPI
from azure.eventhub import EventHubConsumerClient
from app.ml.model import predict_risk
from app.db.sql import insert_many
from collections import deque

app = FastAPI()

CONNECTION_STR = os.getenv("EVENTHUB_CONN_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")
CONSUMER_GROUP = "$Default"

events = deque(maxlen=200)

def flush_to_db():
    global db_buffer

    if not db_buffer:
        return

    insert_many(db_buffer)
    print(f"SAVED BATCH: {len(db_buffer)}")

    db_buffer = []

def on_event(partition_context, event):
    data = json.loads(event.body_as_str())

    prediction = predict_risk(data)
    enriched = { **data, **prediction }
    print("RECEIVED + PREDICTED:", enriched)

    # insert_events(enriched)  
    events.append(enriched)

    # keep memory bounded
    # if len(events) > 100:
    #     events.pop(0)

    # flush every 10 events
    if len(db_buffer) >= 10:
        flush_to_db()

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


@app.get("/events")
def get_events():
    return events

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