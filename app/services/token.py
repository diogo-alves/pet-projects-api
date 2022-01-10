from datetime import datetime, timedelta
from typing import Mapping

from fastapi import Depends
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app.core.config import Settings, get_settings
from app.exceptions.exceptions import AuthenticationError


class TokenService:
    def __init__(self, settings: Settings = Depends(get_settings)) -> None:
        self.settings = settings

    def generate_access_token(self, claims: dict) -> str:
        issued_at: datetime = datetime.utcnow()
        lifetime: timedelta = timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRATION_MINUTES
        )
        claims['iat'] = issued_at
        claims['exp'] = issued_at + lifetime
        return jwt.encode(
            claims,
            self.settings.SECRET_KEY,
            self.settings.JWT_SIGNING_ALGORITHM,
        )

    def decode_access_token(self, token: str) -> Mapping:
        try:
            return jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.JWT_SIGNING_ALGORITHM,
            )
        except ExpiredSignatureError as exc:
            raise AuthenticationError('The token has expired.') from exc
        except JWTClaimsError as exc:
            raise AuthenticationError(f'Invalid claims. {exc}') from exc
        except JWTError as exc:
            raise AuthenticationError('Invalid token.') from exc
