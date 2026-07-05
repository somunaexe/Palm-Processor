import os
import pyodbc

CONN_STR = os.getenv("DATABASE_URL")

conn = None

def get_conn():
    global conn
    if conn is None:
        conn = pyodbc.connect(CONN_STR)
    return conn

def insert_many(events):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO sensor_events
        (machine_id, temperature, vibration, pressure, timestamp, risk_score, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            e["machine_id"],
            e["temperature"],
            e["vibration"],
            e["pressure"],
            e["timestamp"],
            e["risk_score"],
            e["status"]
        )
        for e in events
    ])

    conn.commit()
    conn.close()