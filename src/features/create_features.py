# src/features/create_features.py
import pandas as pd
import os

# Archivos de entrada y salida
RAW_CSV = "data/raw/ecommerce_dataset_10000.csv"
PROCESSED_CSV = "data/processed/ecommerce_dataset_10000_cleaned.csv"
PROCESSED_PARQUET = "data/processed/ecommerce_dataset_10000_cleaned.parquet"

# Crear carpeta processed si no existe
os.makedirs("data/processed", exist_ok=True)

# Leer dataset raw
df = pd.read_csv(RAW_CSV)

# -----------------------
# Seleccionar columnas principales
# -----------------------
columns_needed = [
    'country', 'order_date', 'customer_id', 'product_id', 'product_name', 'category',
    'unit_price', 'quantity', 'order_id', 'order_status', 'payment_method',
    'rating', 'review_text', 'review_date'
]

# Mantener solo columnas existentes
columns_present = [c for c in columns_needed if c in df.columns]
df = df[columns_present]

# -----------------------
# Limpieza de datos
# -----------------------
# Convertir tipos
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce') if 'review_date' in df.columns else None
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

# Eliminar filas críticas con valores nulos
df = df.dropna(subset=['country', 'order_date', 'customer_id', 'product_name', 'unit_price', 'quantity'])

# -----------------------
# Feature Engineering
# -----------------------
df['total_price'] = df['unit_price'] * df['quantity']
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day_of_week'] = df['order_date'].dt.day_name()
df['week_of_year'] = df['order_date'].dt.isocalendar().week

# -----------------------
# Guardar dataset procesado
# -----------------------
df.to_csv(PROCESSED_CSV, index=False)
df.to_parquet(PROCESSED_PARQUET, index=False)

print(f"✅ Processed dataset saved with {len(df)} rows: {PROCESSED_CSV} & {PROCESSED_PARQUET}")
