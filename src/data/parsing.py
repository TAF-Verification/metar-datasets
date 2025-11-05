import os

from datetime import datetime
from enum import Enum
from io import TextIOWrapper, StringIO
from typing import List

import pandas as pd
import numpy as np
from rich import print as rprint
from rich.progress import track

from aeromet_py import Metar
from aeromet_py.reports.models.metar import MetarWeather
from aeromet_py.reports.models.base import GroupList, CloudList
from metpy.io import parse_metar_to_dataframe
from pydantic import BaseModel

from ..config import RAW_DATA_DIR


class ProcessedLine(BaseModel):
    date: datetime
    metar: str


def process_line(l: str) -> ProcessedLine:
    l = l.replace("=", "")
    l = l.strip()

    date = l[0:12]
    metar = l[13:]

    date_obj = datetime.strptime(date, "%Y%m%d%H%M")

    parsed_metar_line = ProcessedLine(date=date_obj, metar=metar)
    return parsed_metar_line


class MetarParserType(str, Enum):
    METPY = "metpy"
    AEROMETPY = "aerometpy"


def _handle_weather(weathers: GroupList[MetarWeather]) -> str:
    weather_list: List[str] = []
    for weather in weathers:
        weather_list.append(weather.code)

    length = len(weather_list)
    string = ""
    match length:
        case 0:
            string = ",,"
        case 1:
            string = ",".join(weather_list) + ",,"
        case 2:
            string = ",".join(weather_list) + ","
        case 3:
            string = ",".join(weather_list)
    return string


def _handle_ceiling(clouds: CloudList) -> int | float:
    try:
        return clouds.ceiling.numerator
    except TypeError:
        return np.nan


def metar_to_dataframe_aerometpy(parser_metar_txt: ProcessedLine) -> pd.DataFrame:
    txt = parser_metar_txt.metar
    date = parser_metar_txt.date
    metar = Metar(txt, year=date.year, month=date.month)

    d = metar.as_dict()
    string = (
        f"{metar.time.time.strftime('%Y-%m-%d %H:%M')},"
        f"{metar.wind.direction_in_degrees},"
        f"{metar.wind.speed_in_knot},"
        f"{metar.wind.gust_in_knot},"
        f"{metar.prevailing_visibility.in_meters},"
        f"{metar.prevailing_visibility.cavok.numerator},"
        f"{_handle_weather(metar.weathers)},"
        f"{_handle_ceiling(metar.clouds)},"
        f"{metar.temperatures.temperature_in_celsius},"
        f"{metar.temperatures.dewpoint_in_celsius},"
        f"{metar.pressure.in_inHg}"
    )

    df = pd.read_csv(
        StringIO(string),
        header=None,
        names=[
            "date",
            "wind_dir_deg",
            "wind_speed_kt",
            "wind_gust_kt",
            "visibility_m",
            "is_cavok",
            "weather_1",
            "weather_2",
            "weather_3",
            "is_ceiling",
            "temp_c",
            "dewpoint_c",
            "pressure_inHg",
        ],
    )

    return df


def process_file(
    f: TextIOWrapper,
    parser: MetarParserType = MetarParserType.METPY,
) -> pd.DataFrame:
    metars_df = pd.DataFrame()
    single_metar_df = pd.DataFrame()

    file_basename = os.path.basename(f.name)

    for line in track(
        f.readlines(), description=f"[green]Processing file {file_basename}"
    ):
        if "NIL" in line:
            continue

        processed_line = process_line(line)

        match parser:
            case MetarParserType.METPY:
                single_metar_df = parse_metar_to_dataframe(
                    processed_line.metar,
                    year=processed_line.date.year,
                    month=processed_line.date.month,
                )
            case MetarParserType.AEROMETPY:
                single_metar_df = metar_to_dataframe_aerometpy(processed_line)

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
    parser: MetarParserType = MetarParserType.METPY,
) -> pd.DataFrame:
    several_years_metars_df = pd.DataFrame()

    station_raw_data_dir = RAW_DATA_DIR / f"{station}"

    rprint(f"Using parser: [green]{parser.name}")
    for year in range(initial_year, final_year + 1):
        file_path = station_raw_data_dir / f"{year}.txt"

        try:
            with open(file_path, "r") as f:
                one_year_metars_df = process_file(f, parser=parser)

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
