from collections.abc import Iterable
from pathlib import Path
from urllib.request import urlretrieve

from data_pipeline.config import BASE_URL, DATASET


def build_filename(month: int, year: int) -> str:
    return f"{DATASET}_tripdata_{year}-{month:02d}.parquet"


def download_file(year: int, month: int, output_dir: Path, overwrite: bool) -> Path:
    filename = build_filename(month, year)
    url = f"{BASE_URL}/{filename}"
    destination = output_dir / filename
    if destination.exists() and not overwrite:  # idempotent: reuse local file
        print(f"Skipping download: {destination} already exists.")
        return destination
    output_dir.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, destination)
    return destination


def download_files(
    year: int, months: Iterable[int], output_dir: Path, overwrite: bool
) -> list[Path]:
    return [download_file(year, month, output_dir, overwrite) for month in months]
