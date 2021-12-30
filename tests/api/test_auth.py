import pytest
from fastapi import status

from app.core.config import settings


@pytest.fixture
def url():
    return f'{settings.API_PREFIX}/auth/token'


def test_login_access_token_should_return_token_if_user_credentials_are_valid(
    client, url, user
):
    payload = {
        'username': 'user@mail.com',
        'password': '123456',
    }
    response = client.post(url, data=payload)
    tokens = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert tokens.get('access_token')
    assert tokens.get('token_type') == 'bearer'


def test_login_access_token_should_return_401_if_user_credentials_are_invalid(
    client, url, user
):
    payload = {
        'username': 'user@mail.com',
        'password': 'wrong-password',
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_access_token_should_return_403_if_user_is_inactive(
    client, url, inactive_user
):
    payload = {
        'username': 'user@mail.com',
        'password': '123456',
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
