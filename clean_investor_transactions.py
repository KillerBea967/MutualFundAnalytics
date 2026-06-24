import pandas as pd

investor_transactions = pd.read_csv("data/raw/investor_transactions.csv")

investor_transactions["transaction_date"] = pd.to_datetime(
    investor_transactions["transaction_date"],
    format="%d-%m-%Y"
)

investor_transactions["transaction_type"] = (
    investor_transactions["transaction_type"].str.strip().str.lower()
)

transaction_mapping = {
    "sip": "SIP",
    "lumpsum": "Lumpsum",
    "redemption": "Redemption"
}

investor_transactions["transaction_type"] = (
    investor_transactions["transaction_type"]
    .replace(transaction_mapping)
)

investor_transactions = investor_transactions[
    investor_transactions["amount_inr"] > 0
]

investor_transactions["kyc_status"] = (
    investor_transactions["kyc_status"]
    .str.strip()
    .str.capitalize()
)

valid_kyc = [
    "Verified",
    "Pending"
]

invalid_kyc = investor_transactions[
    investor_transactions["kyc_status"].isin(valid_kyc)
]

investor_transactions = (
    investor_transactions.drop_duplicates()
)

investor_transactions.to_csv(
    "data/processed/investor_transactions_cleaned.csv",
    index=False
)

print("File Created Successfully")