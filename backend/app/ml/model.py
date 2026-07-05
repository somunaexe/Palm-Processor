# import numpy as np

# def predict_risk(sensor_data):
#     temp = sensor_data["temperature"]
#     vib = sensor_data["vibration"]
#     pressure = sensor_data["pressure"]

#     # simple heuristic model (baseline)
#     risk_score = (
#         (temp - 70) * 0.3 +
#         vib * 10 +
#         abs(pressure - 50) * 0.2
#     )

#     return {
#         "risk_score": round(float(risk_score), 2),
#         "status": "HIGH" if risk_score > 30 else "NORMAL"
#     }