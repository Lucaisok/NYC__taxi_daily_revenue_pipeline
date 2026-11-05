from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from data_pipeline import load_data as load_data_module
from data_pipeline.load_data import load_data
from data_pipeline.pipeline import transform


def write_month(path: Path, pickups: list[str], amounts: list[float]) -> Path:
    pd.DataFrame(
        {
            "VendorID": [2] * len(pickups),
            "lpep_pickup_datetime": pd.to_datetime(pickups),
            "total_amount": amounts,
        }
    ).to_parquet(path, index=False)
    return path


def test_transform_combines_files_and_aggregates(tmp_path: Path) -> None:
    january = write_month(
        tmp_path / "jan.parquet",
        # A December 2024 trip that ended up in the January file is dropped.
        ["2024-12-31 23:50", "2025-01-31 10:00", "2025-01-31 11:00"],
        [99.0, 10.0, 5.0],
    )
    february = write_month(
        tmp_path / "feb.parquet",
        # A January trip filed under February is still counted on its own day.
        ["2025-01-31 23:55", "2025-02-01 09:00"],
        [2.0, 7.0],
    )

    result = transform([january, february])

    assert result.to_dict(orient="records") == [
        {"date": date(2025, 1, 31), "daily_revenue": 17.0},
        {"date": date(2025, 2, 1), "daily_revenue": 7.0},
    ]


def test_load_data_writes_parquet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_dir = tmp_path / "processed"
    monkeypatch.setattr(load_data_module, "PROCESSED_DATA_DIR", output_dir)
    df = pd.DataFrame(
        {"date": [date(2025, 1, 1)], "daily_revenue": [15.0]}
    )

    path = load_data(df)

    assert path.parent == output_dir
    assert path.exists()
    pd.testing.assert_frame_equal(pd.read_parquet(path), df)
