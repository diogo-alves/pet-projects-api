import pytest

from app.exceptions import AuthenticationError
from app.services import TokenService


@pytest.fixture
def token_service(settings) -> TokenService:
    return TokenService(settings)


def test_type_of_generated_token(user, token_service):
    claims = {'sub': user.email}
    generated_token = token_service.generate_access_token(claims)
    assert isinstance(generated_token, str)


def test_type_of_decoded_token(user, token_service):
    claims = {'sub': user.email}
    generated_token = token_service.generate_access_token(claims)
    decoded_token = token_service.decode_access_token(generated_token)
    assert isinstance(decoded_token, dict)


def test_valid_token(user, token_service):
    claims = {'sub': user.email}
    generated_token = token_service.generate_access_token(claims)
    decoded_token = token_service.decode_access_token(generated_token)
    assert decoded_token['sub'] == user.email


def test_expired_token(user, token_service, mocker):
    mocker.patch.object(
        token_service.settings,
        'ACCESS_TOKEN_EXPIRATION_MINUTES',
        -1,
    )
    claims = {'sub': user.email}
    token = token_service.generate_access_token(claims)
    with pytest.raises(AuthenticationError, match='The token has expired'):
        token_service.decode_access_token(token)


def test_decoded_token_with_invalid_claim(token_service):
    claims = {'sub': 1}
    token = token_service.generate_access_token(claims)
    with pytest.raises(AuthenticationError, match='Invalid claim'):
        token_service.decode_access_token(token)


def test_invalid_token(user, token_service):
    claims = {'sub': user.email}
    token = token_service.generate_access_token(claims)
    invalid_token = f'{token}-invalid-part'
    with pytest.raises(AuthenticationError, match='Invalid token'):
        token_service.decode_access_token(invalid_token)
