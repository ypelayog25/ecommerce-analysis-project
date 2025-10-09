import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Timestamp para versionado
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Paths con versionado
RAW_DATA = "data/raw/ecommerce_dataset_10000.csv"
PROCESSED_DATA = f"data/processed/ecommerce_dataset_{timestamp}.csv"
FIGURES_DIR = "reports/figures/"
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 1️⃣ Load dataset
df = pd.read_csv(RAW_DATA)

# 2️⃣ Data cleaning
df = df.drop_duplicates()
df.fillna(0, inplace=True)
df.to_csv(PROCESSED_DATA, index=False)

# 3️⃣ Analysis & visualizations
if 'Country' in df.columns and 'Revenue' in df.columns:
    revenue_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(x=revenue_country.index, y=revenue_country.values)
    plt.xticks(rotation=45)
    plt.title("Revenue by Country")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, f"revenue_by_country_{timestamp}.png"))
    plt.close()

if 'Product' in df.columns and 'Revenue' in df.columns:
    top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=top_products.index, y=top_products.values)
    plt.xticks(rotation=45)
    plt.title("Top 10 Products by Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, f"top_products_{timestamp}.png"))
    plt.close()

# 4️⃣ Summary statistics
summary = df.describe(include='all')
summary.to_csv(f"reports/summary_statistics_{timestamp}.csv")

print("✅ Analysis completed. Versioned figures and processed data saved.")
