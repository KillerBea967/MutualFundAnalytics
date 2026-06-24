import pandas as pd

scheme_performance = pd.read_csv(
    "data/raw/scheme_performance.csv"
)

return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

for col in return_columns:
    scheme_performance[col] = pd.to_numeric(
        scheme_performance[col],
        errors="coerce"
    )

invalid_returns = scheme_performance[
    scheme_performance[return_columns]
    .isnull()
    .any(axis=1)
]

print("Rows with invalid returns:")
print(invalid_returns)

scheme_performance["expense_ratio_pct"] = pd.to_numeric(
    scheme_performance["expense_ratio_pct"],
    errors="coerce"
)

invalid_expense_ratio = scheme_performance[
    (scheme_performance["expense_ratio_pct"] < 0.1)
    |
    (scheme_performance["expense_ratio_pct"] > 2.5)
]

print("Invalid expense ratio rows:")
print(invalid_expense_ratio)

scheme_performance = (
    scheme_performance.drop_duplicates()
)

scheme_performance.to_csv(
    "data/processed/scheme_performance_cleaned.csv",
    index=False
)

print("scheme_performance_cleaned.csv saved successfully.")