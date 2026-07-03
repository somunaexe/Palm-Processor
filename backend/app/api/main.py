import os
import json
import threading
from fastapi import FastAPI
from azure.eventhub import EventHubConsumerClient

app = FastAPI()

CONNECTION_STR = os.getenv("EVENTHUB_CONN_STR")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")
CONSUMER_GROUP = "$Default"

latest_events = []

def on_event(partition_context, event):
    data = json.loads(event.body_as_str())
    print("RECEIVED:", data)

    latest_events.append(data)

    # keep memory bounded
    if len(latest_events) > 100:
        latest_events.pop(0)

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
    return latest_events