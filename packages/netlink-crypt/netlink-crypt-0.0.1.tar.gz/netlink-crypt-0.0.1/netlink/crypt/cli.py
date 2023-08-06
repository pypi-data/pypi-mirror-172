import base64
import click
from .crypt import enigma


@click.command()
@click.option(
    "-o", "--output-format", type=click.Choice(["toml", "b64"], case_sensitive=False), help="Bytes by default."
)
@click.argument("value")
def encrypt_secret(value, output_format):
    """
    Encrypt VALUE using current user and machine to determine keys.

    """
    if output_format is None:
        print(enigma(value))
    elif output_format == "toml":
        print([i for i in enigma(value)])
    elif output_format == "b64":
        print(base64.b64encode(enigma(value)).decode())
    else:
        print("unknown format")
