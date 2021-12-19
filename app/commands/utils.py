import secrets

import typer

app = typer.Typer()


@app.command('gensecretkey')
def generate_random_secret_key():
    secret_key = secrets.token_hex(32)
    typer.echo(secret_key)
