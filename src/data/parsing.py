import os

from datetime import datetime
from io import TextIOWrapper
from typing import List

import pandas as pd
from rich import print as rprint
from rich.progress import track

from metpy.io import parse_metar_to_dataframe
from pydantic import BaseModel

from ..config import RAW_DATA_DIR


class ParsedMetarText(BaseModel):
    date: datetime
    metar: str


def process_line(l: str) -> ParsedMetarText:
    l = l.replace("=", "")
    l = l.strip()

    date = l[0:12]
    metar = l[13:]

    date_obj = datetime.strptime(date, "%Y%m%d%H%M")

    parsed_metar_line = ParsedMetarText(date=date_obj, metar=metar)
    return parsed_metar_line


def process_file(f: TextIOWrapper) -> pd.DataFrame:
    metars_df = pd.DataFrame()

    file_basename = os.path.basename(f.name)

    for line in track(
        f.readlines(), description=f"[green]Processing file {file_basename}"
    ):
        if "NIL" in line:
            continue

        parsed_line = process_line(line)

        single_metar_df = parse_metar_to_dataframe(
            parsed_line.metar,
            year=parsed_line.date.year,
            month=parsed_line.date.month,
        )

        metars_df = pd.concat(
            [metars_df, single_metar_df],
            ignore_index=True,
        )

    return metars_df


def process_several_files(
    station: str,
    initial_year: int,
    final_year: int,
    strict: bool = False,
) -> pd.DataFrame:
    several_years_metars_df = pd.DataFrame()

    station_raw_data_dir = RAW_DATA_DIR / f"{station}"

    for year in range(initial_year, final_year + 1):
        file_path = station_raw_data_dir / f"{year}.txt"

        try:
            with open(file_path, "r") as f:
                one_year_metars_df = process_file(f)

            several_years_metars_df = pd.concat(
                [several_years_metars_df, one_year_metars_df],
                ignore_index=True,
            )
        except FileNotFoundError:
            if strict:
                rprint(f"File {file_path} not found stopping process.")
                break
            else:
                rprint(f"File {file_path} not found, skipping...")
                continue

    return several_years_metars_df
