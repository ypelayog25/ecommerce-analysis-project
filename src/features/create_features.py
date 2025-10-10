import os
import pandas as pd

# Paths
CSV_PATH = "data/processed/ecommerce_dataset_10000_cleaned.csv"
PARQUET_PATH = "data/processed/ecommerce_dataset_10000_cleaned.parquet"

def load_source_data():
    """
    Load the dataset from CSV as the official data source.
    Regenerate a valid Parquet file if missing or corrupted.
    """
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"❌ CSV source not found at {CSV_PATH}. Ensure update_dataset.yml generated it.")

    print(f"✅ CSV found: {CSV_PATH} - Loading as source dataset...")
    df = pd.read_csv(CSV_PATH)

    # Validate Parquet or regenerate it if corrupted
    if not os.path.exists(PARQUET_PATH):
        print("⚠ Parquet file missing. Creating new Parquet file...")
        df.to_parquet(PARQUET_PATH, index=False)
        print(f"✅ New Parquet file created: {PARQUET_PATH}")
    else:
        try:
            pd.read_parquet(PARQUET_PATH)
            print("✔ Existing Parquet file is valid.")
        except Exception:
            print("⚠ Parquet file corrupted. Regenerating...")
            df.to_parquet(PARQUET_PATH, index=False)
            print(f"✅ Parquet file regenerated successfully: {PARQUET_PATH}")

    return df

def create_features(df):
    """
    Add calculated fields such as Revenue and OrderMonth for dashboard analytics.
    """
    print("🔧 Creating new features (Revenue, OrderMonth)...")
    df["Revenue"] = df["UnitPrice"] * df["Quantity"]
    df["OrderMonth"] = pd.to_datetime(df["InvoiceDate"]).dt.to_period("M").astype(str)
    return df

def save_outputs(df):
    """
    Save processed dataset back into both Parquet and CSV formats.
    """
    print("💾 Saving updated dataset with features...")
    df.to_parquet(PARQUET_PATH, index=False)
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Saved: {PARQUET_PATH}")
    print(f"✅ Saved: {CSV_PATH}")

if __name__ == "__main__":
    print("🚀 Running feature engineering pipeline...")
    df = load_source_data()
    df = create_features(df)
    save_outputs(df)
    print("🎉 Feature engineering completed successfully!")
