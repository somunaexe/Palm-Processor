import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.database.models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()