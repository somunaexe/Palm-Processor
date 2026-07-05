CREATE TABLE sensor_events (
    id INT IDENTITY(1,1) PRIMARY KEY,
    machine_id VARCHAR(50),
    temperature FLOAT,
    vibration FLOAT,
    pressure FLOAT,
    timestamp DATETIME,

    risk_score FLOAT,
    status VARCHAR(20)
);