import pandas as pd
import pandas.io.sql as psql

from data_pipeline.config import DEFAULT_MONTHS, DEFAULT_YEAR, RAW_DATA_DIR
from data_pipeline.data_ingestion import download_files


def print_info() -> None:
    df = pd.read_parquet(f"{RAW_DATA_DIR}/green_tripdata_2025-01.parquet")
    print("df.info", df.info())
    schema_sql = psql.get_schema(df.head(0), "yellow_taxi")
    print("schema_sql", schema_sql)


def main() -> None:
    parquet_path = download_files(DEFAULT_YEAR, DEFAULT_MONTHS, RAW_DATA_DIR, False)
    # df = pd.read_parquet(parquet_path)
    # print("parquet_path", parquet_path)
    # print(df.head())
    print(parquet_path)


if __name__ == "__main__":
    main()
    # print_info()
