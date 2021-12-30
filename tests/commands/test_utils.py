from typer.testing import CliRunner

from manage import app as manage_command

runner = CliRunner()


def test_gensecretkey_should_return_a_random_hexadecimal_token(
    mocker,
):
    token = '8db7d3f69fc27ab7c7bf8bb768cd0e605456656c50e3a2a34b46fb74b6c48ed2'
    mocker.patch('app.commands.utils.secrets.token_hex', return_value=token)
    cli_args = ['utils', 'gensecretkey']
    result = runner.invoke(manage_command, cli_args)
    assert token in result.output
