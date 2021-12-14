import typer

from app.core.config import settings
from app.database import generate_db_session
from app.exceptions import EmailAlreadyRegistredError
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
    except EmailAlreadyRegistredError as error:
        message = typer.style(
            error.message,
            fg=typer.colors.YELLOW,
            bold=True,
        )
    finally:
        typer.echo(message)


if __name__ == '__main__':
    app()
