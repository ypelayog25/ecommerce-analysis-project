# src/features/create_features.py
"""
Feature Engineering Script
Generates processed dataset for dashboard and analysis.
"""

import pandas as pd
import os

# Input / Output paths
RAW_CSV = "data/raw/ecommerce_dataset_10000.csv"  # Cambia según tu archivo real
PROCESSED_DIR = "data/processed"
PROCESSED_CSV = os.path.join(PROCESSED_DIR, "ecommerce_dataset_10000_cleaned.csv")
PROCESSED_PARQUET = os.path.join(PROCESSED_DIR, "ecommerce_dataset_10000_cleaned.parquet")

# Crear carpeta processed si no existe
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -----------------------
# Load raw dataset
# -----------------------
df = pd.read_csv(RAW_CSV)

# -----------------------
# Feature Engineering
# -----------------------
# Total price
df['total_price'] = df['unit_price'] * df['quantity']

# Convert dates
df['order_date'] = pd.to_datetime(df['order_date'])
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Fill missing values (opcional)
df['country'] = df['country'].fillna("Unknown")
df['product_name'] = df['product_name'].fillna("Unknown Product")
df['customer_id'] = df['customer_id'].fillna("Unknown Customer")

# -----------------------
# Select required columns for dashboard
# -----------------------
columns_required = [
    'country',
    'order_date',
    'customer_id',
    'product_name',
    'unit_price',
    'quantity',
    'total_price'
]

df_features = df[columns_required]

# -----------------------
# Save processed dataset
# -----------------------
df_features.to_csv(PROCESSED_CSV, index=False)
df_features.to_parquet(PROCESSED_PARQUET, index=False)

print(f"✅ Processed dataset saved as CSV and Parquet in {PROCESSED_DIR}")
print(f"Columns: {list(df_features.columns)}")
