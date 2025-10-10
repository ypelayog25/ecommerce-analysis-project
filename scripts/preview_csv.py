import os
import sys
import pandas as pd

csv_path = os.getenv("CSV_PATH", "data/processed/ecommerce_dataset_10000_cleaned.csv")

try:
    df = pd.read_csv(csv_path, nrows=5)
    print("Detected columns:", list(df.columns))
    print(df.head().to_string(index=False))
except Exception as e:
    print("Error reading CSV preview:", e)
    sys.exit(0)
