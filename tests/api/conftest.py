from typing import Callable, Dict

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.database import generate_db_session
from app.main import app


@pytest.fixture
def client(db_session):
    app.dependency_overrides[generate_db_session] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def get_user_authorization_headers(client) -> Callable:
    def _get_user_autorization_headers(
        username: str, password: str
    ) -> Dict[str, str]:
        url = f'{settings.API_PREFIX}/auth/token'
        payload = {'username': username, 'password': password}
        response = client.post(url, data=payload)
        content = response.json()
        token = content.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        return headers

    return _get_user_autorization_headers
