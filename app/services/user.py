from typing import List

from fastapi import Depends

from app import models, schemas
from app.exceptions import EmailAlreadyRegistredError, NotFoundError
from app.repositories import Repository, UserRepository


class UserService:
    def __init__(
        self, repository: Repository = Depends(UserRepository)
    ) -> None:
        self.repository = repository

    def create(self, payload: schemas.UserBase) -> models.User:
        if self._email_exists(payload.email):
            raise EmailAlreadyRegistredError()
        fields = payload.dict()
        user = models.User(**fields)
        return self.repository.add(user)

    def _email_exists(self, email: str) -> bool:
        return self.repository.get(email=email) is not None

    def change_password(self, username: str, new_password: str) -> None:
        user = self.get_by_email(email=username)
        user.password = new_password
        self.repository.update(user)

    def list(self, skip: int, limit: int) -> List[models.User]:
        return self.repository.list(skip, limit)

    def get_by_id(self, id: int) -> models.User:
        user = self.repository.get(id=id)
        if not user:
            raise NotFoundError()
        return user

    def get_by_email(self, email: str) -> models.User:
        user = self.repository.get(email=email)
        if not user:
            raise NotFoundError()
        return user

    def update_by_id(self, id: int, payload: schemas.UserBase) -> models.User:
        user = self.get_by_id(id)
        return self.update(user, payload)

    def update(
        self, user: models.User, payload: schemas.UserBase
    ) -> models.User:
        if user.email != payload.email and self._email_exists(payload.email):
            raise EmailAlreadyRegistredError()
        fields = payload.dict()
        for field, value in fields.items():
            setattr(user, field, value)
        return self.repository.update(user)

    def delete_by_id(self, id: int) -> None:
        user = self.get_by_id(id)
        self.delete(user)

    def delete(self, user: models.User) -> None:
        self.repository.remove(user)
