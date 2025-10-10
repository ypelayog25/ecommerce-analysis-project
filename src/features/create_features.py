# src/features/create_features.py
"""
Feature engineering for ecommerce dataset.
- Loads canonical CSV (official source).
- Regenerates parquet if missing/corrupted.
- Creates revenue, order/month aggregations, customer RFM features and more.
- Saves parquet + csv and a small preview for quick inspection.
"""

import os
from datetime import datetime
import numpy as np
import pandas as pd

CSV_PATH = "data/processed/ecommerce_dataset_10000_cleaned.csv"
PARQUET_OUT = "data/processed/ecommerce_dataset_features.parquet"
CSV_OUT = "data/processed/ecommerce_dataset_features.csv"
PREVIEW_OUT = "data/processed/ecommerce_dataset_features_preview.csv"
COLUMNS_OUT = "reports/columns.txt"

def find_col(df, candidates):
    """Return first matching column in df among candidates (case-insensitive)."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        key = cand.lower()
        if key in cols_lower:
            return cols_lower[key]
    return None

def safe_qcut_score(series, ascending=True, bins=5):
    """
    Convert a numeric series into 1..bins score.
    ascending=True means larger value => higher score.
    For recency (smaller better) call with ascending=False.
    Uses rank fallback if qcut fails (duplicates).
    """
    try:
        # use qcut to make quantiles
        if ascending:
            labels = list(range(1, bins+1))
        else:
            labels = list(range(bins, 0, -1))
        return pd.qcut(series, q=bins, labels=labels, duplicates='drop').astype(int)
    except Exception:
        # fallback: rank-based normalization
        ranks = series.rank(method='average', pct=True).fillna(0)
        if ascending:
            return (ranks * (bins - 1)).round().astype(int) + 1
        else:
            return ((1 - ranks) * (bins - 1)).round().astype(int) + 1

def load_source():
    """Load dataset from CSV (official). If parquet missing/corrupt, regenerate from CSV."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV source not found at {CSV_PATH}. Run update_dataset first.")
    print(f"✅ CSV found: {CSV_PATH} - Loading as source dataset...")
    df = pd.read_csv(CSV_PATH, low_memory=False)
    # ensure consistent column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]
    return df

def ensure_parquet_from_csv(df):
    """Ensure output parquet exists and is valid; (re)write it from df if not."""
    try:
        if os.path.exists(PARQUET_OUT):
            # try to read to validate
            _ = pd.read_parquet(PARQUET_OUT)
            print("✔ Existing features parquet is valid (will be overwritten after processing).")
        else:
            print("⚠ Features parquet does not exist yet. It will be created after processing.")
    except Exception:
        print("⚠ Existing features parquet corrupted. It will be regenerated.")
    # we will write later after processing

def create_features(df):
    """Create derived features robustly using detected column names."""
    # Detect key columns (common variants)
    price_col = find_col(df, ["unit_price", "unitprice", "price", "unit price"])
    qty_col   = find_col(df, ["quantity", "qty", "count", "amount"])
    order_col = find_col(df, ["order_id", "orderid", "invoice_no", "invoice", "order"])
    order_date_col = find_col(df, ["order_date", "orderdate", "invoice_date", "invoice_date", "date"])
    cust_col  = find_col(df, ["customer_id", "customerid", "cust_id", "client_id"])
    product_col = find_col(df, ["product_name", "product", "productname", "product_id"])

    # Validate
    missing = []
    if price_col is None: missing.append("price (unit_price / price)")
    if qty_col is None: missing.append("quantity")
    if order_col is None: missing.append("order id")
    if order_date_col is None: missing.append("order date")
    if cust_col is None: missing.append("customer id")
    if product_col is None: missing.append("product name / id")

    if missing:
        raise KeyError(f"Required columns missing: {missing}. Detected columns: {list(df.columns)}")

    # Coerce numeric
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce').fillna(0.0)
    df[qty_col] = pd.to_numeric(df[qty_col], errors='coerce').fillna(0.0)

    # Revenue per line
    df["revenue"] = df[price_col] * df[qty_col]

    # Parse order date
    df[order_date_col] = pd.to_datetime(df[order_date_col], errors='coerce')

    # Order month (string YYYY-MM)
    df["order_month"] = df[order_date_col].dt.to_period("M").astype(str)

    # Order-level totals (sum revenue per order)
    order_totals = df.groupby(order_col, dropna=False)["revenue"].sum().rename("order_total").reset_index()
    df = df.merge(order_totals, on=order_col, how="left")

    # Customer-level aggregates
    cust_agg = df.groupby(cust_col).agg(
        customer_total_revenue = ("revenue", "sum"),
        customer_order_count = (order_col, lambda s: s.nunique()),
        customer_avg_order_value = ("order_total", "mean"),
        last_order_date = (order_date_col, "max"),
        first_order_date = (order_date_col, "min")
    ).reset_index()

    # Reference date for recency = max order_date in dataset (most recent)
    reference_date = df[order_date_col].max()
    if pd.isna(reference_date):
        reference_date = pd.Timestamp.utcnow()

    cust_agg["recency_days"] = (reference_date - pd.to_datetime(cust_agg["last_order_date"])).dt.days.fillna(9999).astype(int)
    cust_agg["active_days"] = (pd.to_datetime(cust_agg["last_order_date"]) - pd.to_datetime(cust_agg["first_order_date"])).dt.days.fillna(0).astype(int)

    # Frequency metric -> simply order_count
    cust_agg["frequency"] = cust_agg["customer_order_count"].fillna(0).astype(int)
    cust_agg["monetary"] = cust_agg["customer_total_revenue"].fillna(0.0)

    # RFM scoring (1..5)
    cust_agg["recency_score"] = safe_qcut_score(cust_agg["recency_days"], ascending=False, bins=5)
    cust_agg["frequency_score"] = safe_qcut_score(cust_agg["frequency"], ascending=True, bins=5)
    cust_agg["monetary_score"] = safe_qcut_score(cust_agg["monetary"], ascending=True, bins=5)

    cust_agg["RFM_score"] = cust_agg["recency_score"].astype(str) + \
                             cust_agg["frequency_score"].astype(str) + \
                             cust_agg["monetary_score"].astype(str)

    # Merge customer aggregates back to line-level df (useful for dashboard)
    df = df.merge(cust_agg[[cust_col, "customer_total_revenue", "customer_order_count",
                            "customer_avg_order_value", "last_order_date", "recency_days",
                            "frequency", "monetary", "RFM_score"]], on=cust_col, how="left")

    # Product-level metrics
    prod_agg = df.groupby(product_col).agg(
        product_revenue = ("revenue", "sum"),
        product_units = (qty_col, "sum")
    ).reset_index().sort_values("product_revenue", ascending=False)

    # Country-level revenue if country exists
    country_col = find_col(df, ["country", "shipping_country", "ship_country"])
    if country_col:
        country_rev = df.groupby(country_col)["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
    else:
        country_rev = None

    # Save aggregates into folder for dashboard convenience
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Save full enriched dataset (line-level)
    print(f"💾 Saving enriched dataset to {PARQUET_OUT} and {CSV_OUT} ...")
    df.to_parquet(PARQUET_OUT, index=False)
    df.to_csv(CSV_OUT, index=False)

    # Save preview and columns
    df.head(200).to_csv(PREVIEW_OUT, index=False)
    with open(COLUMNS_OUT, "w") as f:
        f.write("\n".join(df.columns.tolist()))

    # Also save customer/product/country summary tables for quick dashboard use
    cust_agg.to_parquet("data/processed/customer_summary.parquet", index=False)
    prod_agg.to_parquet("data/processed/product_summary.parquet", index=False)
    if country_rev is not None:
        country_rev.to_parquet("data/processed/country_revenue.parquet", index=False)

    print("✅ Feature engineering finished.")
    print(f"Summary: {len(df)} rows, {len(df.columns)} columns.")
    return df

if __name__ == "__main__":
    df = load_source()
    ensure_parquet_from_csv(df)
    df = create_features(df)
