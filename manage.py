import typer

from app.commands import users, utils

app = typer.Typer()
app.add_typer(users.app, name='users')
app.add_typer(utils.app, name='utils')


if __name__ == '__main__':
    app()
