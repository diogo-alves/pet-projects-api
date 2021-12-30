import pytest
from typer.testing import CliRunner

from app.core.config import settings
from manage import app as manage_command

runner = CliRunner()


@pytest.fixture
def mock_get_user_service(mocker, user_service):
    mocker.patch(
        'app.commands.users.get_user_service', return_value=user_service
    )


def test_createsuperuser_should_create_a_superuser_with_default_email(
    mock_get_user_service, user_service
):
    cli_args = ['users', 'createsuperuser', '--password', '123456']
    result = runner.invoke(manage_command, cli_args)
    user_created = user_service.get_by_email(settings.DEFAULT_SUPERUSER_EMAIL)
    assert 'Superuser created successfully' in result.output
    assert user_created.is_superuser


def test_createsuperuser_should_create_a_superuser_with_custom_email(
    mock_get_user_service, user_service
):
    superuser_email = 'admin@mail.com'
    cli_args = [
        'users',
        'createsuperuser',
        '--email',
        superuser_email,
        '--password',
        '123456',
    ]
    result = runner.invoke(manage_command, cli_args)
    user_created = user_service.get_by_email(superuser_email)
    assert 'Superuser created successfully' in result.output
    assert user_created.is_superuser


def test_createsuperuser_should_raise_an_error_if_email_format_is_invalid(
    mock_get_user_service, user_service
):
    invalid_email = 'admin@mail'
    cli_args = [
        'users',
        'createsuperuser',
        '--email',
        invalid_email,
        '--password',
        '123456',
    ]
    result = runner.invoke(manage_command, cli_args)
    assert 'Failed to create superuser' in result.output
    assert 'email: value is not a valid email address' in result.output
    assert user_service._email_exists(invalid_email) is False


def test_createsuperuser_should_raise_an_error_if_email_already_exists(
    mock_get_user_service, user_service, superuser
):
    superuser_email = superuser.email
    cli_args = [
        'users',
        'createsuperuser',
        '--email',
        superuser_email,
        '--password',
        '123456',
    ]
    result = runner.invoke(manage_command, cli_args)
    assert 'User with this email already exists' in result.output
    assert user_service._email_exists(superuser_email) is True


def test_changepassword_should_change_user_password(
    mock_get_user_service, user
):
    user_email = user.email
    new_password = 'new-password'
    cli_args = [
        'users',
        'changepassword',
        '--user-email',
        user_email,
        '--new-password',
        new_password,
    ]
    result = runner.invoke(manage_command, cli_args)
    assert 'Password changed successfully' in result.output
    assert user.verify_password(new_password) is True


def test_changepassword_should_raise_an_error_if_user_email_does_not_exist(
    mock_get_user_service, user_service
):
    user_email = 'admin@mail.com'
    cli_args = [
        'users',
        'changepassword',
        '--user-email',
        user_email,
        '--new-password',
        'new-password',
    ]
    result = runner.invoke(manage_command, cli_args)
    assert f'User with email {user_email!r} does not exist' in result.output
    assert user_service._email_exists(user_email) is False
