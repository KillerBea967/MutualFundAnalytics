import requests
import pandas as pd

def data_fetch(code,fund_name):
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    nav_df = pd.DataFrame(data["data"])
    nav_df.to_csv(f"data/raw/{fund_name}.csv", index=False)