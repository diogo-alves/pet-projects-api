from typing import Optional

from fastapi import Depends

from app.exceptions import AuthenticationError, InactiveUserError
from app.models import User
from app.repositories import Repository, UserRepository


class AuthenticationService:
    def __init__(
        self, user_repository: Repository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def authenticate(self, username: str, password: str) -> User:
        user: Optional[User] = self.user_repository.get(email=username)
        if not user or not user.verify_password(password):
            raise AuthenticationError()
        if not user.is_active:
            raise InactiveUserError()
        return user
