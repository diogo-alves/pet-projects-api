import pytest
from fastapi import status

from app.core.config import settings


@pytest.fixture
def base_url() -> str:
    return f'{settings.API_PREFIX}{settings.API_V1_PREFIX}'


def test_register_should_create_user(client, base_url):
    url = f'{base_url}/users/'
    payload = {
        'email': 'user@mail.com',
        'first_name': 'First',
        'last_name': 'Last',
        'password': '123456',
    }
    response = client.post(url, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert content['id']
    assert content['email'] == payload['email']
    assert content['first_name'] == payload['first_name']
    assert content['last_name'] == payload['last_name']
    assert content['is_active'] is True
    assert content['is_superuser'] is False


def test_register_should_return_409_if_email_has_taken(client, base_url, user):
    url = f'{base_url}/users/'
    payload = {
        'email': 'user@mail.com',
        'first_name': 'First',
        'last_name': 'Last',
        'password': '123456',
    }
    response = client.post(url, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert content['detail'] == 'User with this email already exists.'


def test_list_all_should_return_list_of_users_if_current_user_is_a_superuser(
    client, base_url, get_user_authorization_headers, users
):
    url = f'{base_url}/users/'
    superuser = users[0]
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == len(users)


def test_list_all_should_allow_to_skip_users(
    client, base_url, get_user_authorization_headers, users
):
    skipped_users = 1
    url = f'{base_url}/users?skip={skipped_users}'
    headers = get_user_authorization_headers(
        username='user1@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == len(users) - skipped_users


def test_list_all_should_allow_to_limit_the_number_of_users_returned(
    client, base_url, get_user_authorization_headers, users
):
    limit_of_users_returned = 2
    url = f'{base_url}/users?limit={limit_of_users_returned}'
    headers = get_user_authorization_headers(
        username='user1@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == limit_of_users_returned


def test_list_all_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_list_all_should_return_403_if_current_user_is_not_a_superuser(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert content['detail'] == 'Permission denied.'


def test_retrieve_logged_should_return_the_current_user(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == user.first_name
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active
    assert content['is_superuser'] == user.is_superuser


def test_retrieve_logged_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_update_logged_should_update_the_current_user(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {
        'email': user.email,
        'first_name': 'New First Name',
        'last_name': user.last_name,
        'is_active': user.is_active,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == payload['first_name']
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active


def test_update_logged_should_allow_partial_update_of_user_data(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {'first_name': 'New First Name'}
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == payload['first_name']
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active


def test_update_logged_should_allow_user_to_deactivate_account(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {
        'is_active': False,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['is_active'] is False


def test_update_logged_should_not_alow_user_to_grant_himself_superuser_access(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {'is_superuser': True}
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['is_superuser'] is False


def test_update_logged_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.put(url, headers=headers, json={})
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_delete_logged_should_allow_to_delete_the_current_user(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_logged_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/me'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.delete(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_retrieve_should_return_a_user_if_current_user_is_a_superuser(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == user.first_name
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active
    assert content['is_superuser'] == user.is_superuser


def test_retrieve_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='wrong-password'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_retrieve_should_return_403_if_current_user_is_not_a_superuser(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{superuser.id}'
    headers = get_user_authorization_headers(user.email, password='123456')
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert content['detail'] == 'Permission denied.'


def test_retrieve_should_return_404_if_user_does_not_exist(
    client, base_url, get_user_authorization_headers, superuser
):
    invalid_user_id = 999
    url = f'{base_url}/users/{invalid_user_id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content['detail'] == 'Not found.'


def test_update_should_return_a_user_updated_if_current_user_is_a_superuser(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    payload = {
        'email': user.email,
        'first_name': 'New First Name',
        'last_name': user.last_name,
        'is_active': False,
        'is_superuser': True,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == payload['first_name']
    assert content['last_name'] == user.last_name
    assert content['is_active'] == payload['is_active']
    assert content['is_superuser'] == payload['is_superuser']


def test_update_should_allow_partial_update_of_user_data(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    payload = {'first_name': 'New First Name'}
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == user.id
    assert content['email'] == user.email
    assert content['first_name'] == payload['first_name']
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active
    assert content['is_superuser'] == user.is_superuser


def test_update_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.put(url, headers=headers, json={})
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_update_should_return_403_if_current_user_is_not_a_superuser(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.put(url, headers=headers, json={})
    content = response.json()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert content['detail'] == 'Permission denied.'


def test_update_should_return_404_if_user_does_not_exist(
    client, base_url, get_user_authorization_headers, superuser
):
    invalid_user_id = 999
    url = f'{base_url}/users/{invalid_user_id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.put(url, headers=headers, json={})
    content = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content['detail'] == 'Not found.'


def test_delete_should_return_204_if_user_was_deleted(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{user.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='wrong-password'
    )
    response = client.delete(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert content['detail'] == 'Invalid token.'


def test_delete_should_return_403_if_current_user_is_not_a_superuser(
    client, base_url, get_user_authorization_headers, user, superuser
):
    url = f'{base_url}/users/{superuser.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert content['detail'] == 'Permission denied.'


def test_delete_should_return_404_if_user_does_not_exist(
    client, base_url, get_user_authorization_headers, superuser
):
    invalid_user_id = 999
    url = f'{base_url}/users/{invalid_user_id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content['detail'] == 'Not found.'
