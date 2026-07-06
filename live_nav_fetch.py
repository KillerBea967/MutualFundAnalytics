import requests
import pandas as pd

def data_fetch(code,fund_name):
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    nav_df = pd.DataFrame(data["data"])
    nav_df.to_csv(f"data/raw/doc/{fund_name}.csv", index=False)

schemes = {
    "SBI_Mutual_Fund":125497,
    "SBI_Bluechip":119551,
    "ICICI_Bluechip":120503,
    "Nippon_LargeCap":118632,
    "Axis_Bluechip":119092,
    "Kotak_Bluechip":120841
}

for fund_name, code in schemes.items():
    data_fetch(code,fund_name)