import pandas as pd

fund_master = pd.read_csv("./data/raw/doc/fund_master.csv")
nav_history = pd.read_csv("./data/raw/doc/nav_history.csv")

with open("mined_data.txt", "w", encoding="utf-8") as mined_data:

    mined_data.write("UNIQUE FUND HOUSES\n")
    for house in fund_master["fund_house"].unique():
        mined_data.write(f"{house}\n")

    mined_data.write("\n")

    mined_data.write("UNIQUE CATEGORIES\n")
    for category in fund_master["category"].unique():
        mined_data.write(f"{category}\n")

    mined_data.write("\n")

    mined_data.write("UNIQUE SUB-CATEGORIES\n")
    for sub_category in fund_master["sub_category"].unique():
        mined_data.write(f"{sub_category}\n")

    mined_data.write("\n")

    mined_data.write("UNIQUE RISK CATEGORIES\n")
    for risk in fund_master["risk_category"].unique():
        mined_data.write(f"{risk}\n")

    mined_data.write("\n")

    master_codes = set(fund_master["amfi_code"])
    nav_codes = set(nav_history["amfi_code"])

    missing_codes = master_codes - nav_codes

    mined_data.write("AMFI CODE VALIDATION\n")
    mined_data.write(f"Total codes in fund_master : {len(master_codes)}\n")
    mined_data.write(f"Total codes in nav_history : {len(nav_codes)}\n")
    mined_data.write(f"Missing codes : {len(missing_codes)}\n\n")

    if len(missing_codes) > 0:
        mined_data.write("Missing AMFI Codes:\n")
        for code in missing_codes:
            mined_data.write(f"{code}\n")
    else:
        mined_data.write("All AMFI codes in fund_master are present in nav_history.\n")

    mined_data.write("\n")

print("Report saved as mined_data.txt")