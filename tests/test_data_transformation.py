from datetime import date

import pandas as pd

from data_pipeline.data_transformation import (
    filter_columns,
    filter_dates,
    get_daily_revenue,
)


def make_trips(pickups: list[str], amounts: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "lpep_pickup_datetime": pd.to_datetime(pickups),
            "total_amount": amounts,
        }
    )


def test_filter_columns_keeps_only_needed_columns() -> None:
    df = make_trips(["2025-01-01 08:00"], [10.0]).assign(
        VendorID=[2], trip_distance=[3.1]
    )

    result = filter_columns(df)

    assert list(result.columns) == ["lpep_pickup_datetime", "total_amount"]


def test_filter_dates_keeps_only_q1_2025() -> None:
    df = make_trips(
        [
            "2024-12-31 23:59",  # before the period
            "2025-01-01 00:00",  # first moment of the period
            "2025-03-31 23:59",  # last day of the period
            "2025-04-01 00:00",  # after the period
        ],
        [1.0, 2.0, 3.0, 4.0],
    )

    result = filter_dates(df)

    assert result["total_amount"].tolist() == [2.0, 3.0]


def test_get_daily_revenue_sums_per_day() -> None:
    df = make_trips(
        ["2025-01-01 08:00", "2025-01-01 21:30", "2025-01-02 14:00"],
        [10.5, 4.5, 15.0],
    )

    result = get_daily_revenue(df)

    assert result.to_dict(orient="records") == [
        {"date": date(2025, 1, 1), "daily_revenue": 15.0},
        {"date": date(2025, 1, 2), "daily_revenue": 15.0},
    ]


def test_get_daily_revenue_reversal_pair_nets_to_zero() -> None:
    df = make_trips(
        ["2025-01-01 08:00", "2025-01-01 08:00", "2025-01-01 12:00"],
        [25.0, -25.0, 10.0],
    )

    result = get_daily_revenue(df)

    assert result["daily_revenue"].tolist() == [10.0]
