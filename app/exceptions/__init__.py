from fastapi import FastAPI

from .exceptions import (
    AuthenticationError,
    EmailAlreadyRegistredError,
    InactiveUserError,
    NotFoundError,
    PermissionDeniedError,
)
from .handlers import (
    authentication_exception_handler,
    email_already_registred_exception_handler,
    inactive_user_exception_handler,
    not_found_exception_handler,
    permission_denied_exception_handler,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, not_found_exception_handler)

    app.add_exception_handler(
        EmailAlreadyRegistredError, email_already_registred_exception_handler
    )
    app.add_exception_handler(
        AuthenticationError, authentication_exception_handler
    )
    app.add_exception_handler(
        InactiveUserError, inactive_user_exception_handler
    )
    app.add_exception_handler(
        PermissionDeniedError, permission_denied_exception_handler
    )
