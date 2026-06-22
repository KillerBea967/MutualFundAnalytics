import requests
import pandas as pd
from data_fetch import data_fetch

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