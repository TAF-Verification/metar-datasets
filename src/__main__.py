import os

from typing import Annotated, Optional
from datetime import datetime

import typer

from rich import print as rprint

from .__version__ import __version__
from .config import PROCESSED_DATA_DIR, INITIAL_DATA_YEAR
from .data import process_several_files


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


@app.command("to-csv")
def create_csv_file(
    station: Annotated[
        str,
        typer.Argument(
            case_sensitive=True, help="ICAO for the station data to process."
        ),
    ] = "mroc",
    initial_year: Annotated[
        int,
        typer.Option("--init", "-i", help="Initial year to process raw data."),
    ] = INITIAL_DATA_YEAR,
    final_year: Annotated[
        Optional[int],
        typer.Option(
            "--final",
            "-f",
            help="Final year to process raw data. Current year if not given.",
        ),
    ] = None,
    strict: Annotated[
        bool,
        typer.Option(
            "--strict-mode/--no-strict-mode",
            "-s/-S",
            help="Breaks the reading data process if a file is not found.",
        ),
    ] = False,
) -> None:
    station = station.lower()

    if not final_year:
        final_year = datetime.now().year

    rprint(
        f"Processing raw data files from {initial_year} to {final_year} for station {station.upper()}."
    )
    metars_df = process_several_files(
        station,
        initial_year=initial_year,
        final_year=final_year,
        strict=strict,
    )

    save_path = PROCESSED_DATA_DIR / f"{station}/metar/csv/"
    os.makedirs(save_path, exist_ok=True)

    metars_df.to_csv(save_path / "metars.csv")
    rprint(f"CSV file created successfully for station {station.upper()}.")
    rprint(f"File saved at {save_path}.")


if __name__ == "__main__":
    app()
