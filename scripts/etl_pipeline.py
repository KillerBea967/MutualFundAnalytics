import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

project_root = Path(__file__).resolve().parent.parent

processed_folder = project_root / "data" / "processed"
database_folder = project_root / "data" / "db"
sql_folder = project_root / "sql"

database_folder.mkdir(exist_ok=True)

db_path = database_folder / "bluestock_mf.db"

engine = create_engine(f"sqlite:///{db_path}")

with open(sql_folder / "schema.sql", "r") as file:
    schema = file.read()

with engine.begin() as conn:
    conn.execute(text(schema))

fund_master = pd.read_csv(processed_folder / "fund_master_clean.csv")

nav_history = pd.read_csv(processed_folder / "nav_history_clean.csv")

transactions = pd.read_csv(
    processed_folder / "investor_transactions_clean.csv"
)

performance = pd.read_csv(
    processed_folder / "scheme_performance_clean.csv"
)

aum = pd.read_csv(
    processed_folder / "aum_by_fund_house_clean.csv"
)

nav_history["date"] = pd.to_datetime(nav_history["date"])

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

aum["date"] = pd.to_datetime(aum["date"])

dim_fund = fund_master[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "sub_category",
        "plan",
        "fund_manager",
        "risk_category"
    ]
]

all_dates = pd.concat([
    nav_history["date"],
    transactions["transaction_date"],
    aum["date"]
]).drop_duplicates().sort_values().reset_index(drop=True)

dim_date = pd.DataFrame({
    "date": all_dates
})

dim_date["date_id"] = (
    dim_date["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

dim_date["year"] = dim_date["date"].dt.year
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.month_name()
dim_date["day"] = dim_date["date"].dt.day
dim_date["weekday_name"] = dim_date["date"].dt.day_name()
dim_date["is_weekend"] = (
    dim_date["date"].dt.weekday >= 5
).astype(int)

fact_nav = nav_history.merge(
    dim_date[["date", "date_id"]],
    on="date",
    how="left"
)

fact_nav = fact_nav[
    [
        "amfi_code",
        "date_id",
        "nav"
    ]
]

fact_transactions = transactions.merge(
    dim_date[["date", "date_id"]],
    left_on="transaction_date",
    right_on="date",
    how="left"
)

fact_transactions = fact_transactions[
    [
        "investor_id",
        "date_id",
        "amfi_code",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
]

fact_performance = performance[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "morningstar_rating"
    ]
]

fact_aum = aum.merge(
    dim_date[["date", "date_id"]],
    on="date",
    how="left"
)

fact_aum = fact_aum[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
]

dim_fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

fact_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

fact_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

tables = {
    "dim_fund": dim_fund,
    "dim_date": dim_date,
    "fact_nav": fact_nav,
    "fact_transactions": fact_transactions,
    "fact_performance": fact_performance,
    "fact_aum": fact_aum
}

print("\nRow Count Verification")
print("-" * 40)

for table, df in tables.items():
    db_count = pd.read_sql(
        f"SELECT COUNT(*) AS count FROM {table}",
        engine
    ).iloc[0, 0]

    print(f"{table:<20} CSV={len(df):>6} | DB={db_count:>6}")

print("\nETL Pipeline Completed Successfully!")