from typing import Optional, Annotated

import typer
from rich import print

from .__version__ import __version__


app = typer.Typer()


def version_callback(version: bool) -> None:
    if version:
        print(f"metar-datasets, version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            help="Show module version and exit.",
        ),
    ] = None,
) -> None:
    print("metar-datasets CLI")


if __name__ == "__main__":
    app()
