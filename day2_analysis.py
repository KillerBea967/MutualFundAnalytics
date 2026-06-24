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

    f.write("\nANALYTICAL SQL QUERIES AND RESULTS\n")
    f.write("-" * 60 + "\n")

    queries = {

        "1. Top 5 Funds by 5-Year Return":
        """
        SELECT
            df.scheme_name,
            fp.return_5yr_pct
        FROM fact_performance fp
        JOIN dim_fund df
        ON fp.amfi_code = df.amfi_code
        ORDER BY fp.return_5yr_pct DESC
        LIMIT 5
        """,

        "2. Average NAV per Month":
        """
        SELECT
            strftime('%Y-%m', date) AS month,
            ROUND(AVG(nav),2) AS avg_nav
        FROM fact_nav
        GROUP BY month
        ORDER BY month
        """,

        "3. SIP Year-wise Growth":
        """
        SELECT
            strftime('%Y', transaction_date) AS year,
            ROUND(SUM(amount_inr),2) AS total_sip_amount
        FROM fact_transactions
        WHERE transaction_type = 'SIP'
        GROUP BY year
        ORDER BY year
        """,

        "4. Transactions by State":
        """
        SELECT
            state,
            COUNT(*) AS total_transactions
        FROM fact_transactions
        GROUP BY state
        ORDER BY total_transactions DESC
        """,

        "5. Funds with Expense Ratio < 1%":
        """
        SELECT
            df.scheme_name,
            fp.expense_ratio_pct
        FROM fact_performance fp
        JOIN dim_fund df
        ON fp.amfi_code = df.amfi_code
        WHERE fp.expense_ratio_pct < 1
        ORDER BY fp.expense_ratio_pct
        """,

        "6. Top 10 Funds by 3-Year Return":
        """
        SELECT
            df.scheme_name,
            fp.return_3yr_pct
        FROM fact_performance fp
        JOIN dim_fund df
        ON fp.amfi_code = df.amfi_code
        ORDER BY fp.return_3yr_pct DESC
        LIMIT 10
        """,

        "7. Top 10 Funds by Sharpe Ratio":
        """
        SELECT
            df.scheme_name,
            fp.sharpe_ratio
        FROM fact_performance fp
        JOIN dim_fund df
        ON fp.amfi_code = df.amfi_code
        ORDER BY fp.sharpe_ratio DESC
        LIMIT 10
        """,

        "8. Total Investment by Gender":
        """
        SELECT
            gender,
            ROUND(SUM(amount_inr),2)
        FROM fact_transactions
        GROUP BY gender
        """,

        "9. Transaction Count by Payment Mode":
        """
        SELECT
            payment_mode,
            COUNT(*)
        FROM fact_transactions
        GROUP BY payment_mode
        ORDER BY COUNT(*) DESC
        """,

        "10. Average 5-Year Return by Category":
        """
        SELECT
            df.category,
            ROUND(AVG(fp.return_5yr_pct),2)
        FROM fact_performance fp
        JOIN dim_fund df
        ON fp.amfi_code = df.amfi_code
        GROUP BY df.category
        ORDER BY AVG(fp.return_5yr_pct) DESC
        """
    }

    for title, query in queries.items():

        f.write(f"\n{title}\n")
        f.write("-" * len(title) + "\n")

        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            f.write(str(row) + "\n")

        f.write("\n")

conn.close()
print("Day 2 outcomes saved successfully to day2_outcomes.txt")