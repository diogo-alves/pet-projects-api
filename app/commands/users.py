import typer
from pydantic import ValidationError

from app.core.config import settings
from app.database import generate_db_session
from app.exceptions import EmailAlreadyRegistredError, NotFoundError
from app.repositories import UserRepository
from app.schemas import FullUserIn
from app.services import UserService

app = typer.Typer()


def get_user_service():
    db = next(generate_db_session())
    user_repository = UserRepository(db)
    return UserService(user_repository)


@app.command('createsuperuser')
def create_superuser(
    email: str = typer.Option(settings.DEFAULT_SUPERUSER_EMAIL, prompt=True),
    password: str = typer.Option(
        ...,
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
    ),
) -> None:
    user_service = get_user_service()
    message = ''
    try:
        superuser = FullUserIn(
            email=email,
            password=password,
            is_superuser=True,
        )
        user_service.create(superuser)
        message = typer.style(
            'Superuser created successfully.',
            fg=typer.colors.GREEN,
            bold=True,
        )
    except ValidationError as exc:
        errors = '\n'.join(
            f'  {error["loc"][0]}: {error["msg"]}' for error in exc.errors()
        )
        message = typer.style(
            f'Failed to create superuser:\n{errors}',
            fg=typer.colors.RED,
            bold=True,
        )
    except EmailAlreadyRegistredError as exc:
        message = typer.style(
            exc.message,
            fg=typer.colors.YELLOW,
            bold=True,
        )
    finally:
        typer.echo(message)


@app.command('changepassword')
def change_password(
    user_email: str = typer.Option(..., prompt=True),
    new_password: str = typer.Option(
        ...,
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
    ),
) -> None:
    user_service = get_user_service()
    message = ''
    try:
        user_service.change_password(user_email, new_password)
        message = typer.style(
            'Password changed successfully.',
            fg=typer.colors.GREEN,
            bold=True,
        )
    except NotFoundError:
        message = typer.style(
            f'User with email {user_email!r} does not exist.',
            fg=typer.colors.RED,
            bold=True,
        )
    finally:
        typer.echo(message)


if __name__ == '__main__':
    app()
