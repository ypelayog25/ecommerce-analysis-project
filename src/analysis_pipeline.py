import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
RAW_DATA = "data/raw/ecommerce_dataset_10000.csv"
PROCESSED_DATA = "data/processed/ecommerce_dataset_10000_cleaned.csv"
FIGURES_DIR = "reports/figures/"

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 1️⃣ Load dataset
df = pd.read_csv(RAW_DATA)

# 2️⃣ Data cleaning example
# - Remove duplicates
df = df.drop_duplicates()
# - Fill missing values if any (example)
df.fillna(0, inplace=True)

# Save cleaned dataset
df.to_csv(PROCESSED_DATA, index=False)

# 3️⃣ Analysis & visualizations

# Example: Revenue by Country
if 'Country' in df.columns and 'Revenue' in df.columns:
    revenue_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(x=revenue_country.index, y=revenue_country.values)
    plt.xticks(rotation=45)
    plt.title("Revenue by Country")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "revenue_by_country.png"))
    plt.close()

# Example: Top Products
if 'Product' in df.columns and 'Revenue' in df.columns:
    top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=top_products.index, y=top_products.values)
    plt.xticks(rotation=45)
    plt.title("Top 10 Products by Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "top_products.png"))
    plt.close()

# 4️⃣ Summary statistics for Tableau or reporting
summary = df.describe(include='all')
summary.to_csv("reports/summary_statistics.csv")

print("✅ Analysis completed. Figures and processed data saved.")
