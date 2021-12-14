from fastapi import Request, status
from fastapi.responses import JSONResponse

from .exceptions import (
    AuthenticationError,
    EmailAlreadyRegistredError,
    InactiveUserError,
    NotFoundError,
    PermissionDeniedError,
)


def not_found_exception_handler(
    request: Request, exc: NotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={'detail': exc.message}
    )


def email_already_registred_exception_handler(
    request: Request, exc: EmailAlreadyRegistredError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'detail': exc.message},
    )


def authentication_exception_handler(
    request: Request, exc: AuthenticationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'WWW-Authenticate': 'Bearer'},
        content={'detail': exc.message},
    )


def inactive_user_exception_handler(
    request: Request, exc: InactiveUserError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'detail': exc.message},
    )


def permission_denied_exception_handler(
    request: Request, exc: PermissionDeniedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'detail': exc.message},
    )
