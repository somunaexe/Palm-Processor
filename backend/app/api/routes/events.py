from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.database.database import get_db
from app.adapters.database.sql_repository import SqlSensorRepository

router = APIRouter()


@router.get("/events/latest")
def get_latest_events(db: Session = Depends(get_db)):

    repo = SqlSensorRepository(db)

    return repo.get_latest(limit=50)