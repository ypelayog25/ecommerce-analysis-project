# scripts/verify_columns.py
"""
Verify that the processed dataset contains all required columns
"""

import pandas as pd
import sys
import os

DATA_FILE = "data/processed/ecommerce_dataset_10000_cleaned.parquet"

REQUIRED_COLUMNS = [
    'country',
    'order_date',
    'customer_id',
    'product_name',
    'unit_price',
    'quantity',
    'total_price'
]

# Check if dataset exists
if not os.path.exists(DATA_FILE):
    print(f"❌ Dataset not found: {DATA_FILE}")
    sys.exit(1)

try:
    df = pd.read_parquet(DATA_FILE)
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    sys.exit(1)

# Check missing columns
missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

if missing:
    print(f"❌ Missing required columns: {missing}")
    sys.exit(1)
else:
    print("✅ All required columns are present.")
