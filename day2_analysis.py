import pandas as pd

scheme_performance = pd.read_csv(
    "data/processed/scheme_performance_cleaned.csvv"
)

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

print("Rows with invalid returns:")
print(invalid_returns)

invalid_expense_ratio = scheme_performance[
    (scheme_performance["expense_ratio_pct"] < 0.1)
    |
    (scheme_performance["expense_ratio_pct"] > 2.5)
]

print("Invalid expense ratio rows:")
print(invalid_expense_ratio)