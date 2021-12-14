from typing import Any, List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from app.database import generate_db_session


class UserRepository:
    def __init__(self, db: Session = Depends(generate_db_session)) -> None:
        self.db = db

    def add(self, obj: models.User) -> models.User:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self, skip: int, limit: int) -> List[models.User]:
        return self.db.query(models.User).offset(skip).limit(limit).all()

    def filter(
        self, skip: int, limit: int, **kwargs: Any
    ) -> List[models.User]:
        return (
            self.db.query(models.User)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, **kwargs: Any) -> Optional[models.User]:
        return self.db.query(models.User).filter_by(**kwargs).first()

    def update(self, obj: models.User) -> models.User:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def remove(self, obj: models.User) -> None:
        self.db.delete(obj)
        self.db.commit()
