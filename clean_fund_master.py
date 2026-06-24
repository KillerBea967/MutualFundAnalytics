import pandas as pd

fund_master = pd.read_csv("data/raw/fund_master.csv")

fund_master["launch_date"] = pd.to_datetime(
    fund_master["launch_date"],
    dayfirst=True,
    errors="coerce"
)

numeric_cols = [
    "amfi_code",
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount"
]

for col in numeric_cols:
    fund_master[col] = pd.to_numeric(
        fund_master[col],
        errors="coerce"
    )

text_cols = [
    "fund_house",
    "scheme_name",
    "category",
    "sub_category",
    "plan",
    "benchmark",
    "fund_manager",
    "risk_category",
    "sebi_category_code"
]

for col in text_cols:
    fund_master[col] = (
        fund_master[col]
        .astype(str)
        .str.strip()
    )

fund_master = fund_master.drop_duplicates()

fund_master.to_csv(
    "data/processed/fund_master_cleaned.csv",
    index=False
)

print("File Created Successfully")