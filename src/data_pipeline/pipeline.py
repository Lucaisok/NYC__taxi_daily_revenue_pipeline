from pathlib import Path

import pandas as pd

from data_pipeline.config import (
    DEFAULT_MONTHS,
    DEFAULT_YEAR,
    RAW_DATA_DIR,
)
from data_pipeline.data_ingestion import download_files
from data_pipeline.data_transformation import (
    filter_columns,
    filter_dates,
    get_daily_revenue,
)
from data_pipeline.load_data import load_data


def extract_files() -> list[Path]:
    return download_files(DEFAULT_YEAR, DEFAULT_MONTHS, RAW_DATA_DIR, False)


def transform_data(paths: list[Path]) -> pd.DataFrame:
    df = pd.concat(
        [pd.read_parquet(path) for path in paths],
        ignore_index=True,
    )
    filtered_cols_df = filter_columns(df)
    filtered_dates_df = filter_dates(filtered_cols_df)
    daily_revenue_df = get_daily_revenue(filtered_dates_df)
    return daily_revenue_df


def pipeline() -> None:
    parquet_paths = extract_files()
    df = transform_data(parquet_paths)
    load_data(df)


if __name__ == "__main__":
    pipeline()
