import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///mutual_fund.db")

fund_master = pd.read_csv("data/processed/fund_master_cleaned.csv")
nav_history = pd.read_csv("data/processed/nav_history_cleaned.csv")
transactions = pd.read_csv("data/processed/investor_transactions_cleaned.csv")
performance = pd.read_csv("data/processed/scheme_performance_cleaned.csv")
aum = pd.read_csv("data/processed/aum_by_fund_house_cleaned.csv")

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

dim_fund.to_sql(
"dim_fund",
engine,
if_exists="replace",
index=False
)

nav_history.to_sql(
"fact_nav",
engine,
if_exists="replace",
index=False
)

transactions.to_sql(
"fact_transactions",
engine,
if_exists="replace",
index=False
)

performance.to_sql(
"fact_performance",
engine,
if_exists="replace",
index=False
)

aum.to_sql(
"fact_aum",
engine,
if_exists="replace",
index=False
)