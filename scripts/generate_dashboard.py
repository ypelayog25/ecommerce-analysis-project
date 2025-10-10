"""
generate_dashboard.py
Generates dashboard charts (PNG) from processed e-commerce dataset.
"""

import os
import sys
import pandas as pd
import plotly.express as px

def main():
    try:
        # Paths for processed dataset
        dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"
        dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"

        # Load dataset
        if os.path.exists(dataset_parquet):
            df = pd.read_parquet(dataset_parquet)
            print(f"✅ Loaded dataset from {dataset_parquet}")
        elif os.path.exists(dataset_csv):
            df = pd.read_csv(dataset_csv)
            print(f"✅ Loaded dataset from {dataset_csv}")
        else:
            print("❌ Processed dataset not found.")
            sys.exit(1)

        # Ensure figures folder exists
        figures_folder = "reports/figures"
        os.makedirs(figures_folder, exist_ok=True)

        # Helper to check columns
        def has_columns(columns):
            missing = [col for col in columns if col not in df.columns]
            return missing

        # 1️⃣ Revenue by Country
        missing = has_columns(['country', 'total_price'])
        if not missing:
            fig_country = px.bar(
                df.groupby('country')['total_price'].sum().reset_index(),
                x='country', y='total_price', title='Revenue by Country'
            )
            fig_country.write_image(os.path.join(figures_folder, "revenue_by_country.png"))
            print("✅ revenue_by_country.png generated")
        else:
            print(f"⚠️ Missing columns for country revenue chart: {missing}")

        # 2️⃣ Monthly Revenue
        missing = has_columns(['order_date', 'total_price'])
        if not missing:
            df['order_date'] = pd.to_datetime(df['order_date'])
            monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
            monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
            fig_monthly = px.line(monthly, x='order_date', y='total_price', title='Monthly Revenue')
            fig_monthly.write_image(os.path.join(figures_folder, "monthly_revenue.png"))
            print("✅ monthly_revenue.png generated")
        else:
            print(f"⚠️ Missing columns for monthly revenue chart: {missing}")

        # 3️⃣ Top 10 Customers
        missing = has_columns(['customer_id', 'total_price'])
        if not missing:
            top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(10).reset_index()
            fig_customers = px.bar(top_customers, x='customer_id', y='total_price', title='Top 10 Customers')
            fig_customers.write_image(os.path.join(figures_folder, "top_customers.png"))
            print("✅ top_customers.png generated")
        else:
            print(f"⚠️ Missing columns for top customers chart: {missing}")

        # 4️⃣ Top 10 Products
        missing = has_columns(['product_name', 'quantity'])
        if not missing:
            top_products = df.groupby('product_name')['quantity'].sum().nlargest(10).reset_index()
            fig_products = px.bar(top_products, x='product_name', y='quantity', title='Top 10 Products')
            fig_products.write_image(os.path.join(figures_folder, "top_products.png"))
            print("✅ top_products.png generated")
        else:
            print(f"⚠️ Missing columns for top products chart: {missing}")

        # 5️⃣ Unit Price Distribution
        missing = has_columns(['unit_price'])
        if not missing:
            fig_price = px.histogram(df, x='unit_price', nbins=50, title='Unit Price Distribution')
            fig_price.write_image(os.path.join(figures_folder, "unit_price_distribution.png"))
            print("✅ unit_price_distribution.png generated")
        else:
            print(f"⚠️ Missing columns for unit price distribution chart: {missing}")

    except Exception as e:
        print(f"⚠️ Dashboard generation error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
