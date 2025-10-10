# src/visualization/save_figures.py
"""
Generate static PNG previews for key charts.
Uses Plotly with Kaleido to write image files.
"""

import os
import pandas as pd
import plotly.express as px

OUT_DIR = "reports/figures"
os.makedirs(OUT_DIR, exist_ok=True)

FEAT_PARQUET = "data/processed/ecommerce_dataset_features.parquet"
if not os.path.exists(FEAT_PARQUET):
    raise FileNotFoundError(f"Features parquet not found at {FEAT_PARQUET}. Run feature engineering first.")

df = pd.read_parquet(FEAT_PARQUET)

# Monthly revenue
if "order_month" in df.columns and "revenue" in df.columns:
    monthly = df.groupby("order_month")["revenue"].sum().reset_index()
    fig = px.line(monthly, x="order_month", y="revenue", title="Revenue Over Time - Monthly")
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue")
    fig.write_image(os.path.join(OUT_DIR, "monthly_revenue.png"))
    print("Saved monthly_revenue.png")

# Top 10 products
prod_col = next((c for c in ["product_name", "product", "product_name".lower()] if c in df.columns), None)
if prod_col is None:
    prod_col = [c for c in df.columns if "product" in c.lower()]
    prod_col = prod_col[0] if prod_col else None

if prod_col and "revenue" in df.columns:
    top_products = df.groupby(prod_col)["revenue"].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x="revenue", y=prod_col, orientation="h", title="Top 10 Products by Revenue")
    fig.write_image(os.path.join(OUT_DIR, "top_products.png"))
    print("Saved top_products.png")

# Revenue by country
country_col = next((c for c in df.columns if "country" in c.lower()), None)
if country_col and "revenue" in df.columns:
    country_rev = df.groupby(country_col)["revenue"].sum().reset_index()
    fig = px.choropleth(country_rev, locations=country_col, locationmode="country names", color="revenue",
                        title="Revenue by Country")
    fig.write_image(os.path.join(OUT_DIR, "revenue_by_country.png"))
    print("Saved revenue_by_country.png")

# Customer segments distribution
if "RFM_score" in df.columns:
    rfm = df.groupby("RFM_score")["revenue"].sum().reset_index()
    fig = px.bar(rfm, x="RFM_score", y="revenue", title="Revenue by RFM Score")
    fig.write_image(os.path.join(OUT_DIR, "revenue_by_rfm.png"))
    print("Saved revenue_by_rfm.png")

print("✅ All preview images generated (if data available).")
