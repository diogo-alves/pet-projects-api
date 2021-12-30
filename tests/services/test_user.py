import pytest

from app.exceptions import EmailAlreadyRegistredError, NotFoundError
from app.models import User
from app.schemas import UserBase


def test_create_user_should_return_an_user(user_service):
    payload = UserBase(email='user@mail.com')
    user_created = user_service.create(payload)
    assert isinstance(user_created, User)


def test_email_exists(user_service, user):
    assert user_service._email_exists(user.email) is True


def test_create_user_should_raise_an_error_if_email_already_exists(
    user_service, user
):
    payload = UserBase(email=user.email)
    with pytest.raises(EmailAlreadyRegistredError):
        user_service.create(payload)


def test_get_user_by_id_should_return_user(user_service, user):
    assert user_service.get_by_id(user.id) == user


def test_get_user_by_id_should_raise_an_error_if_user_does_not_exist(
    user_service, user
):
    with pytest.raises(NotFoundError):
        user_service.get_by_id(999)


def test_get_user_by_email_should_return_user(user_service, user):
    assert user_service.get_by_email(user.email) == user


def test_get_user_by_email_should_raise_an_error_if_user_does_not_exist(
    user_service, user
):
    with pytest.raises(NotFoundError):
        user_service.get_by_email('does_not_exists@mail.com')


def test_change_password(user_service, user):
    user_service.change_password(
        username=user.email, new_password='new-password'
    )
    assert user.verify_password('new-password') is True


def test_list_users(user_service, users):
    result = user_service.list(skip=0, limit=10)
    assert len(result) == 3


def test_update_user_should_return_the_user_updated(user_service, user):
    payload = UserBase(email=user.email, first_name='Other')
    user_updated = user_service.update(user, payload)
    assert user_updated.id == user.id
    assert user_updated.first_name == payload.first_name


def test_update_user_should_raise_an_error_if_email_already_exists(
    user_service, users
):
    payload = UserBase(email=users[0].email)
    with pytest.raises(EmailAlreadyRegistredError):
        user_service.update(users[1], payload)


def test_update_user_by_id_should_return_the_user_updated(user_service, user):
    payload = UserBase(email=user.email, first_name='Other')
    user_updated = user_service.update_by_id(user.id, payload)
    assert user_updated.id == user.id
    assert user_updated.first_name == payload.first_name


def test_delete_user(user_service, user):
    user_service.delete(user)
    assert user not in user_service.list(skip=0, limit=10)


def test_delete_user_by_id(user_service, user):
    user_service.delete_by_id(user.id)
    assert user not in user_service.list(skip=0, limit=10)
