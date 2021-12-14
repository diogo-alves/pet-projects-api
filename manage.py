import typer

from app.commands import users

app = typer.Typer()
app.add_typer(users.app, name='users')


if __name__ == '__main__':
    app()
