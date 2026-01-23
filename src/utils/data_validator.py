import pandas as pd
from typing import List, Set


REQUIRED_STATION_COLS = {'station_code', 'station_name', 'state', 'zone'}
REQUIRED_TRAIN_COLS = {'train_no', 'from_code', 'to_code', 'train_name'}


def missing_columns(df: pd.DataFrame, required: set) -> List[str]:
    return [c for c in required if c not in df.columns]


def find_missing_station_codes(trains_df: pd.DataFrame, stations_df: pd.DataFrame) -> Set[str]:
    if trains_df is None or trains_df.empty or stations_df is None or stations_df.empty:
        return set()

    station_codes = set(stations_df['station_code'].astype(str).str.upper()) if 'station_code' in stations_df.columns else set()
    from_codes = set(trains_df['from_code'].astype(str).str.upper()) if 'from_code' in trains_df.columns else set()
    to_codes = set(trains_df['to_code'].astype(str).str.upper()) if 'to_code' in trains_df.columns else set()

    used = from_codes.union(to_codes)
    missing = {c for c in used if c and c not in station_codes}
    return missing


def validate_stations_df(stations_df: pd.DataFrame) -> List[str]:
    return missing_columns(stations_df, REQUIRED_STATION_COLS)


def validate_trains_df(trains_df: pd.DataFrame) -> List[str]:
    return missing_columns(trains_df, REQUIRED_TRAIN_COLS)
