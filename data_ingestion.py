import pandas as pd
import os

path = "./data/raw"

csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]

for file in csv_files:
    print("="*60)
    print("FILE:", file)

    df = pd.read_csv(os.path.join(path, file))

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())
