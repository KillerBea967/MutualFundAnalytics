import pandas as pd
import os

# Load CSV files
csv_files = [f for f in os.listdir("./data/raw/doc") if f.endswith(".csv")]

# Load specific datasets
fund_master = pd.read_csv("./data/raw/fund_master.csv")
nav_history = pd.read_csv("./data/raw/nav_history.csv")

# Open a single output file
with open("day1_outcomes.txt", "w", encoding="utf-8") as output_file:

    output_file.write("DAY 1: DATA INGESTION SUMMARY\n\n")

    for file in csv_files:
        df = pd.read_csv(os.path.join("./data/raw/doc", file))

        text = (
            f"FILE: {file}\n\n"
            "Shape:\n"
            f"{df.shape}\n\n"
            "Data Types:\n"
            f"{df.dtypes}\n\n"
            "First 5 Rows:\n"
            f"{df.head()}\n\n"
        )

        output_file.write(text)

    output_file.write("FUND MASTER EXPLORATION\n")

    output_file.write("UNIQUE FUND HOUSES\n")
    for house in fund_master["fund_house"].unique():
        output_file.write(f"{house}\n")

    output_file.write("\nUNIQUE CATEGORIES\n")
    for category in fund_master["category"].unique():
        output_file.write(f"{category}\n")

    output_file.write("\nUNIQUE SUB-CATEGORIES\n")
    for sub_category in fund_master["sub_category"].unique():
        output_file.write(f"{sub_category}\n")

    output_file.write("\nUNIQUE RISK CATEGORIES\n")
    for risk in fund_master["risk_category"].unique():
        output_file.write(f"{risk}\n")

    master_codes = set(fund_master["amfi_code"])
    nav_codes = set(nav_history["amfi_code"])

    missing_codes = master_codes - nav_codes

    output_file.write("AMFI CODE VALIDATION\n")

    output_file.write(f"Total codes in fund_master : {len(master_codes)}\n")
    output_file.write(f"Total codes in nav_history : {len(nav_codes)}\n")
    output_file.write(f"Missing codes : {len(missing_codes)}\n\n")

    if len(missing_codes) > 0:
        output_file.write("Missing AMFI Codes:\n")
        for code in missing_codes:
            output_file.write(f"{code}\n")
    else:
        output_file.write("All AMFI codes in fund_master are present in nav_history.\n")

    output_file.write("DAY 1 Work Summary\n")

    output_file.write(
        "- Successfully loaded all datasets.\n"
        "- Explored fund houses, categories, sub-categories and risk categories.\n"
        "- AMFI codes uniquely identify mutual fund schemes.\n"
    )

print("Day 1 outcomes saved successfully to day1_outcomes.txt")