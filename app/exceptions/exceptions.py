from typing import Optional


class BaseAppException(Exception):
    default_message = ''

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(BaseAppException):
    default_message = 'Not found.'


class EmailAlreadyRegistredError(BaseAppException):
    default_message = 'User with this email already exists.'


class AuthenticationError(BaseAppException):
    default_message = 'Invalid credentials.'


class InactiveUserError(BaseAppException):
    default_message = 'Inactive user.'


class PermissionDeniedError(BaseAppException):
    default_message = 'Permission denied.'
