# NYC Green Taxi – Daily Revenue Pipeline

An ETL pipeline that downloads the NYC [Green Taxi trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) for January–March 2025 and calculates the total revenue per day.

## Running it

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.13 (see [`.python-version`](.python-version)).

```bash
uv sync
uv run python -m data_pipeline.pipeline
```

The result is written to `data/processed/daily_revenue_2025_q1.parquet`: 90 rows, one per day from 2025-01-01 to 2025-03-31, with the columns `date` and `daily_revenue`.

Raw files that already exist in `data/raw/` are not downloaded again, so running the pipeline a second time skips the download.

To run the tests:

```bash
uv run pytest
```

Only the `tests/` folder is collected (set with `testpaths` in [`pyproject.toml`](pyproject.toml)), so the separate `solution/` tests are not run.

### Viewing runs in the Prefect UI

The pipeline is a [Prefect](https://docs.prefect.io/) flow. Without a server it runs as normal and logs to the terminal. To see each run, its steps and their logs in a dashboard, start a local Prefect server in a second terminal before running the pipeline:

```bash
uv run prefect server start
```

Then open http://127.0.0.1:4200.

## How it works

The pipeline has three stages. In [`pipeline.py`](src/data_pipeline/pipeline.py) each stage is a Prefect task (`extract`, `transform`, `load`), and the `nyc-taxi-daily-revenue` flow runs them in order:

| Stage | Module | What it does |
| --- | --- | --- |
| Extract | [`data_ingestion.py`](src/data_pipeline/data_ingestion.py) | Downloads the monthly Parquet files to `data/raw/` (the staging area). |
| Transform | [`data_transformation.py`](src/data_pipeline/data_transformation.py) | Combines the three months, keeps only `lpep_pickup_datetime` and `total_amount`, drops trips with a pickup date outside Q1 2025, and sums `total_amount` per pickup date. |
| Load | [`load_data.py`](src/data_pipeline/load_data.py) | Writes the daily revenue table to `data/processed/` as Parquet. |

The year, months, URLs and paths are set in [`config.py`](src/data_pipeline/config.py).

The modules hold plain Python functions; only `pipeline.py` uses Prefect. This keeps the logic easy to unit test. The extract task retries up to 3 times, 10 seconds apart, because the download is a network call that can fail temporarily.

## Why ETL and not ELT

In **ETL** (extract, transform, load), the data is transformed *before* it is saved to its destination. In **ELT** (extract, load, transform), the raw data is first loaded into the destination, usually a data warehouse, and then transformed there, often with SQL.

This pipeline is ETL. The transformation is done in Python with pandas, and only the final 90-row table is saved. That fits this project:

- The data is small enough (about 146,000 trips) to process in memory on a laptop.
- There is no warehouse to load raw data into, and none is needed for one daily metric.
- Only the aggregated result is used, so there is no reason to store the raw data a second time.

ELT would make more sense if the data were much larger, or if other people needed to run different queries on the raw trips inside a warehouse.

## Data notes

- **Pickup dates outside the file's month.** Each monthly file contains a few trips (73 in total) with a pickup date in a neighbouring month, for example December 2024 trips in the January file. The three files are combined before filtering, so a trip that is in the wrong file but still falls in Q1 is counted on its correct day. Only trips with a pickup date outside January–March 2025 are dropped.
- **Negative `total_amount` values.** 478 trips have a negative `total_amount`. 475 of them have a matching positive trip with the same pickup time and the same amount, so they are reversals of a charge. They are **kept on purpose**: in the daily sum, each pair cancels to zero, which correctly counts a voided trip as no revenue. Dropping only the negative rows would leave the positive half and overstate revenue.

## Project questions

### 1. What steps did I take to complete the project?

1. Wrote the extract step to download the three monthly files to a local staging directory, skipping files that already exist.
2. Explored the downloaded data in [`notebooks/data_exploration.ipynb`](notebooks/data_exploration.ipynb) to understand the columns and spot data quality issues.
3. Wrote the transform step: select the needed columns, filter to the target date range, and aggregate revenue per day.
4. Wrote the load step to save the result to `data/processed/`.
5. Split the code into separate extract, transform and load modules and connected them in a single pipeline entry point.
6. Turned the pipeline into a Prefect flow, with each stage as a task and retries on the download step.

### 2. What challenges did I face?

_TODO_

### 3. What would I do differently with more time?

_TODO_
