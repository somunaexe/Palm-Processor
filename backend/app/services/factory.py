from sqlalchemy.orm import Session

from app.services.sensor_service import SensorService
from app.services.prediction_service import PredictionService
from app.adapters.database.sql_repository import SqlSensorRepository


def create_sensor_service(db: Session) -> SensorService:

    sql_sensor_repository = SqlSensorRepository(db)
    prediction_service = PredictionService()

    return SensorService(
        sensor_repository=sql_sensor_repository,
        prediction_service=prediction_service,
    )