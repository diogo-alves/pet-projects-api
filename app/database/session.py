from typing import Generator

from sqlalchemy.orm import sessionmaker

from .config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def generate_db_session() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
