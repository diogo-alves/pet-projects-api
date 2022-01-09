from datetime import datetime, timedelta
from typing import Mapping

from fastapi import Depends
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app.core.config import Settings, get_settings
from app.exceptions.exceptions import AuthenticationError


class TokenService:
    def __init__(self, settings: Settings = Depends(get_settings)) -> None:
        self.secret = settings.SECRET_KEY
        self.algorithm = settings.JWT_SIGNING_ALGORITHM
        self.issuer = settings.APP_NAME
        self.issued_at = datetime.utcnow()
        self.lifetime = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES
        )
        self.expiration_time = self.issued_at + self.lifetime

    def generate_access_token(self, claims: dict) -> str:
        claims['iat'] = self.issued_at
        claims['exp'] = self.expiration_time
        claims['iss'] = self.issuer
        return jwt.encode(claims, self.secret, self.algorithm)

    def decode_access_token(self, token: str) -> Mapping:
        try:
            return jwt.decode(token, self.secret, self.algorithm)
        except ExpiredSignatureError as exc:
            raise AuthenticationError('The token has expired.') from exc
        except JWTClaimsError as exc:
            raise AuthenticationError(f'Invalid claims. {exc}') from exc
        except JWTError as exc:
            raise AuthenticationError('Invalid token.') from exc
