import pandas as pd
import sqlite3
conn = sqlite3.connect("mutual_fund.db")
cursor = conn.cursor()


fund_master = pd.read_csv("data/processed/fund_master_cleaned.csv")
nav_history = pd.read_csv("data/processed/nav_history_cleaned.csv")
investor_transactions = pd.read_csv("data/processed/investor_transactions_cleaned.csv")
scheme_performance = pd.read_csv("data/processed/scheme_performance_cleaned.csv")
aum = pd.read_csv("data/processed/aum_by_fund_house_cleaned.csv")

sql_counts = {}
tables = [
    "dim_fund",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    sql_counts[table] = cursor.fetchone()[0]

valid_kyc = ["Verified", "Pending"]

invalid_kyc = investor_transactions[
    investor_transactions["kyc_status"].isin(valid_kyc)
]

return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

invalid_returns = scheme_performance[
    scheme_performance[return_columns]
    .isnull()
    .any(axis=1)
]

invalid_expense_ratio = scheme_performance[
    (scheme_performance["expense_ratio_pct"] < 0.1) | (scheme_performance["expense_ratio_pct"] > 2.5)
]

with open("reports/day2_outcomes.txt", "w", encoding="utf-8") as f:

    f.write("DAY 2 OUTCOMES\n\n")

    f.write("ROW COUNT VERIFICATION\n")
    f.write(f"dim_fund : CSV = {len(fund_master)} | SQL = {sql_counts['dim_fund']}\n")
    f.write(f"fact_nav : CSV = {len(nav_history)} | SQL = {sql_counts['fact_nav']}\n")
    f.write(f"fact_transactions : CSV = {len(investor_transactions)} | SQL = {sql_counts['fact_transactions']}\n")
    f.write(f"fact_performance : CSV = {len(scheme_performance)} | SQL = {sql_counts['fact_performance']}\n")
    f.write(f"fact_aum : CSV = {len(aum)} | SQL = {sql_counts['fact_aum']}\n\n")

    f.write("TABLE KEYS\n")
    f.write(
        "dim_fund\n"
        "Primary Key : amfi_code\n\n"
    )
    f.write(
        "fact_nav\n"
        "Primary Key : nav_id\n"
        "Foreign Key : amfi_code -> dim_fund(amfi_code)\n\n"
    )
    f.write(
        "fact_transactions\n"
        "Primary Key : transaction_id\n"
        "Foreign Key : amfi_code -> dim_fund(amfi_code)\n\n"
    )
    f.write(
        "fact_performance\n"
        "Primary Key : performance_id\n"
        "Foreign Key : amfi_code -> dim_fund(amfi_code)\n\n"
    )
    f.write(
        "fact_aum\n"
        "Primary Key : aum_id\n\n"
    )

    f.write("DATA VALIDATION RESULTS\n")
    f.write("-" * 60 + "\n")

    f.write(
        f"Invalid KYC rows in Transactions : {len(invalid_kyc)}\n"
    )

    f.write(
        f"Rows with invalid returns in Performance : {len(invalid_returns)}\n"
    )

    f.write(
        f"Rows with invalid expense ratio in Performance : {len(invalid_expense_ratio)}\n\n"
    )

conn.close()
print("Day 2 outcomes saved successfully to day2_outcomes.txt")