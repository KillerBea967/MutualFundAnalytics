import pandas as pd

aum = pd.read_csv("data/raw/aum_by_fund_house.csv")

aum["date"] = pd.to_datetime(
    aum["date"],
    dayfirst=True,
    errors="coerce"
)

numeric_cols = [
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]

for col in numeric_cols:
    aum[col] = pd.to_numeric(
        aum[col],
        errors="coerce"
    )

aum["fund_house"] = (
    aum["fund_house"]
    .astype(str)
    .str.strip()
)

aum = aum.drop_duplicates()

aum.to_csv(
    "data/processed/aum_by_fund_house_cleaned.csv",
    index=False
)

print("File Created Successfully")