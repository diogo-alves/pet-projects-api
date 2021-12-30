import pytest

from app.exceptions import AuthenticationError, InactiveUserError
from app.services import AuthenticationService


@pytest.fixture
def auth_service(user_repository):
    return AuthenticationService(user_repository)


def test_authenticate_should_return_the_user_authenticated(auth_service, user):
    user_authenticated = auth_service.authenticate(
        username=user.email, password='123456'
    )
    assert user_authenticated == user


def test_authenticate_should_raise_an_error_if_user_does_not_exist(
    auth_service,
):
    with pytest.raises(AuthenticationError):
        auth_service.authenticate(username='user@mail.com', password='123456')


def test_authenticate_should_raise_an_error_if_password_is_invalid(
    auth_service, user
):
    with pytest.raises(AuthenticationError):
        auth_service.authenticate(username=user.email, password='wrong-pass')


def test_authenticate_should_raise_an_error_if_user_is_inactive(
    auth_service, inactive_user
):
    with pytest.raises(InactiveUserError):
        auth_service.authenticate(
            username=inactive_user.email, password='123456'
        )
