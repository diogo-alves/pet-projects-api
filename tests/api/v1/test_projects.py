import pytest
from fastapi import status

from app.core.config import settings


@pytest.fixture
def base_url():
    return f'{settings.API_PREFIX}{settings.API_V1_PREFIX}/projects'


def test_create_should_create_a_new_project_if_current_user_is_authenticated(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    payload = {
        'title': 'New Project',
        'description': 'An awesome new project',
        'url': 'https://newproject.com',
    }
    response = client.post(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert content['title'] == payload['title']
    assert content['description'] == payload['description']
    assert content['url'] == payload['url']
    assert content['owner']['id'] == user.id


def test_create_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user
):
    url = f'{base_url}/'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='wrong-password'
    )
    payload = {
        'title': 'New Project',
        'description': 'An awesome new project',
        'url': 'https://newproject.com',
    }
    response = client.post(url, headers=headers, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_all_should_return_a_list_of_projects(
    client, base_url, get_user_authorization_headers, projects
):
    url = f'{base_url}/'
    headers = get_user_authorization_headers(
        username='user1@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == len(projects)


def test_list_all_should_allow_to_skip_projects(
    client, base_url, get_user_authorization_headers, projects
):
    url = f'{base_url}?skip=1'
    headers = get_user_authorization_headers(
        username='user1@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == len(projects) - 1


def test_list_all_should_allow_to_limit_the_number_of_projects_returned(
    client, base_url, get_user_authorization_headers, projects
):
    url = f'{base_url}?limit=2'
    headers = get_user_authorization_headers(
        username='user1@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == len(projects) - 1


def test_list_all_should_return_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, projects
):
    url = base_url
    headers = get_user_authorization_headers(
        username='invalid_user@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_retrieve_should_retrieve_a_project_if_exists(
    client, base_url, get_user_authorization_headers, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['id'] == project.id


def test_retrieve_should_return_404_if_project_does_not_exist(
    client, base_url, get_user_authorization_headers, user
):
    invalid_project_id = '999'
    url = f'{base_url}/{invalid_project_id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_should_update_project_if_current_user_is_authenticated(
    client, base_url, get_user_authorization_headers, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    payload = {
        'title': f'{project.title} was changed',
        'description': project.description,
        'url': project.url,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['title'] == payload['title']


def test_update_should_update_project_if_current_user_is_owner(
    client, base_url, get_user_authorization_headers, user, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    payload = {
        'title': f'{project.title} was changed',
        'description': project.description,
        'url': project.url,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert user.id == project.owner_id
    assert content['id'] == project.id
    assert content['title'] == payload['title']


def test_update_should_update_project_if_current_user_is_superuser(
    client, base_url, get_user_authorization_headers, superuser, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    payload = {
        'title': f'{project.title} was changed',
        'description': project.description,
        'url': project.url,
    }
    response = client.put(url, headers=headers, json=payload)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert superuser.is_superuser
    assert superuser.id != project.owner_id
    assert content['id'] == project.id
    assert content['title'] == payload['title']


def test_update_should_raise_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='wrong-password'
    )
    payload = {
        'title': f'{project.title} was changed',
        'description': project.description,
        'url': project.url,
    }
    response = client.put(url, headers=headers, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_should_raise_403_if_current_user_has_not_permission_to_update(
    client, base_url, get_user_authorization_headers, users, projects
):
    user = users[2]
    project = projects[0]
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {
        'title': f'{project.title} was changed',
        'description': project.description,
        'url': project.url,
    }
    response = client.put(url, headers=headers, json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert user.id != project.owner_id
    assert user.is_superuser is False


def test_update_should_raise_404_if_project_does_not_exist(
    client, base_url, get_user_authorization_headers, user
):
    invalid_project_id = 999
    url = f'{base_url}/{invalid_project_id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    payload = {
        'title': 'A title',
        'description': 'A description',
        'url': 'http://fakeurl.com',
    }
    response = client.put(url, headers=headers, json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_should_delete_project_if_current_user_is_authenticated(
    client, base_url, get_user_authorization_headers, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username='user@mail.com', password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_should_delete_project_if_current_user_is_owner(
    client, base_url, get_user_authorization_headers, user, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.id == project.owner_id


def test_delete_should_delete_project_if_current_user_is_superuser(
    client, base_url, get_user_authorization_headers, superuser, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=superuser.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert superuser.is_superuser is True
    assert superuser.id != project.owner_id


def test_delete_should_raise_401_if_credentials_are_invalid(
    client, base_url, get_user_authorization_headers, user, project
):
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='wrong-password'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_should_raise_403_if_current_user_has_not_permission_to_delete(
    client, base_url, get_user_authorization_headers, users, projects
):
    user = users[2]
    project = projects[0]
    url = f'{base_url}/{project.id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert user.id != project.owner_id
    assert user.is_superuser is False


def test_delete_should_raise_404_if_project_does_not_exist(
    client, base_url, get_user_authorization_headers, user
):
    invalid_project_id = 999
    url = f'{base_url}/{invalid_project_id}'
    headers = get_user_authorization_headers(
        username=user.email, password='123456'
    )
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
