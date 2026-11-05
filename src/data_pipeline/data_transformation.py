import pandas as pd

selected_columns = ["lpep_pickup_datetime", "total_amount"]


def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[selected_columns]


def filter_dates(df: pd.DataFrame) -> pd.DataFrame:
    period = df["lpep_pickup_datetime"]
    return df[(period >= "2025-01-01") & (period < "2025-04-01")]


def get_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    # Negative total_amount rows are kept on purpose: almost all are reversals
    # of a positive trip with the same pickup time and amount, so the pair
    # nets to zero in the sum. Dropping only the negatives would overstate revenue.
    return (
        df.assign(date=df["lpep_pickup_datetime"].dt.date)
        .groupby("date", as_index=False)
        .agg(daily_revenue=("total_amount", "sum"))
    )
