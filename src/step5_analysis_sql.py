import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path("./")
DATA_PATH = PROJECT_ROOT / "data" / "features" / "ecommerce_features.csv"
REPORTS_PATH = PROJECT_ROOT / "reports" / "figures"
REPORTS_PATH.mkdir(parents=True, exist_ok=True)

# --- Load dataset ---
df = pd.read_csv(DATA_PATH)
print(f"✅ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")

# --- Connect to DuckDB ---
con = duckdb.connect(database=':memory:')
con.register("ecommerce", df)

# --- 1. Top 10 customers by revenue ---
query_top_clients = '''
SELECT customer_id,
       SUM(quantity * unit_price) AS total_revenue,
       COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10
'''
top_clients = con.execute(query_top_clients).df()

plt.figure(figsize=(10,5))
plt.bar(top_clients['customer_id'], top_clients['total_revenue'])
plt.xticks(rotation=45)
plt.title("Top 10 Customers by Revenue")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "top_clients.png")
plt.close()

# --- 2. Top 10 products sold ---
query_top_products = '''
SELECT product_name,
       SUM(quantity) AS total_sold
FROM ecommerce
GROUP BY product_name
ORDER BY total_sold DESC
LIMIT 10
'''
top_products = con.execute(query_top_products).df()

plt.figure(figsize=(10,5))
plt.bar(top_products['product_name'], top_products['total_sold'])
plt.xticks(rotation=60)
plt.title("Top 10 Best-Selling Products")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "top_products.png")
plt.close()

# --- 3. Revenue by country ---
query_country_revenue = '''
SELECT country,
       SUM(quantity * unit_price) AS total_revenue
FROM ecommerce
GROUP BY country
ORDER BY total_revenue DESC
'''
country_revenue = con.execute(query_country_revenue).df()

plt.figure(figsize=(8,5))
plt.barh(country_revenue['country'], country_revenue['total_revenue'])
plt.title("Total Revenue by Country")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "revenue_by_country.png")
plt.close()

# --- 4. Monthly revenue evolution ---
query_sales_time = '''
SELECT strftime('%Y-%m', CAST(order_date AS DATE)) AS month,
       SUM(quantity * unit_price) AS monthly_revenue
FROM ecommerce
GROUP BY month
ORDER BY month
'''
sales_time = con.execute(query_sales_time).df()

plt.figure(figsize=(10,5))
plt.plot(sales_time['month'], sales_time['monthly_revenue'], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Revenue Evolution")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "sales_over_time.png")
plt.close()

# --- Export SQL Insights Report ---
summary_path = PROJECT_ROOT / "reports" / "SQL_Insights.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("🔍 SQL Insights Summary\n")
    f.write("="*40 + "\n\n")
    f.write("Top 10 Customers:\n")
    f.write(top_clients.to_string(index=False))
    f.write("\n\nTop 10 Products:\n")
    f.write(top_products.to_string(index=False))
    f.write("\n\nRevenue by Country:\n")
    f.write(country_revenue.to_string(index=False))

print("\n✅ SQL Insights generated successfully!")
print(f"📊 Reports saved in: {REPORTS_PATH}")
