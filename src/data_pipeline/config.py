from pathlib import Path

DEFAULT_YEAR = 2025
DEFAULT_MONTHS = (1, 2, 3)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DATASET = "green"

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

PROCESSED_FILE_NAME = "daily_revenue_2025_q1.parquet"
