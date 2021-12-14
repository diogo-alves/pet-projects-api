from datetime import datetime, timedelta
from typing import Mapping

from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from passlib.context import CryptContext

from app.exceptions.exceptions import AuthenticationError

from .config import settings

password_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])
SIGNING_ALGORITHM = ALGORITHMS.HS256


def hash_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def check_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def generate_access_token(
    claims: dict,
    lifetime: timedelta = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES
    ),
) -> str:
    now = datetime.utcnow()
    claims['iat'] = now
    claims['exp'] = now + lifetime
    claims['iss'] = settings.APP_NAME
    return jwt.encode(claims, settings.SECRET_KEY, SIGNING_ALGORITHM)


def decode_access_token(token: str) -> Mapping:
    try:
        return jwt.decode(token, settings.SECRET_KEY, SIGNING_ALGORITHM)
    except ExpiredSignatureError as exc:
        raise AuthenticationError('The token has expired.') from exc
    except JWTClaimsError as exc:
        raise AuthenticationError(f'Invalid claims. {exc}') from exc
    except JWTError as exc:
        raise AuthenticationError('Invalid token.') from exc
