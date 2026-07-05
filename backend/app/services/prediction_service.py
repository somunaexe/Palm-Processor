from app.domain.models import SensorEvent, Prediction


class PredictionService:

    def predict(self, event: SensorEvent) -> Prediction:

        risk_score = (
            (event.temperature - 70) * 0.3 +
            event.vibration * 10 +
            abs(event.pressure - 50) * 0.2
        )

        status = "HIGH" if risk_score > 30 else "NORMAL"

        return Prediction(
            risk_score=round(float(risk_score), 2),
            status=status
        )