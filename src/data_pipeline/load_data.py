from pathlib import Path

import pandas as pd

from data_pipeline.config import PROCESSED_DATA_DIR, PROCESSED_FILE_NAME


def load_data(df: pd.DataFrame) -> Path:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DATA_DIR / PROCESSED_FILE_NAME
    df.to_parquet(path, index=False)
    return path
