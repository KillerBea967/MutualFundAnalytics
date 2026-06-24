import pandas as pd

nav_history = pd.read_csv("data/raw/nav_history.csv")

nav_history["date"] = pd.to_datetime(
    nav_history["date"],
    format="%d-%m-%Y"
)

nav_history = nav_history.sort_values(
    by=["amfi_code", "date"]
)

nav_history["nav"] = (
    nav_history.groupby("amfi_code")["nav"]
    .ffill()
)

nav_history = nav_history.drop_duplicates()

nav_history = nav_history[
    nav_history["nav"] > 0
]

nav_history.to_csv("data/processed/nav_history_cleaned.csv",index=False)