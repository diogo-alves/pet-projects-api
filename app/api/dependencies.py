from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.security import decode_access_token
from app.exceptions import PermissionDeniedError
from app.models import User
from app.services import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_PREFIX}/auth/token'
)


def get_current_user(
    token: str = Depends(oauth2_scheme), user_service: UserService = Depends()
):
    claims = decode_access_token(token)
    user_email = claims.get('sub', '')
    return user_service.get_by_email(user_email)


def get_current_superuser(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise PermissionDeniedError()
    return current_user
