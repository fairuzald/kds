from typing import Generator
from sqlalchemy.orm import Session as SQLAlchemySession
from app.db.session import SessionLocal

def get_db() -> Generator[SQLAlchemySession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
