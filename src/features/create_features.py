import pandas as pd
from src.data.load_dataset import load_dataset

def add_features(df):
    """
    Add calculated features to the dataset.
    """
    # Revenue per order
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    # Extract order month for time series
    df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.to_period('M')
    return df

if __name__ == "__main__":
    # Load dataset
    df = load_dataset()
    # Add features
    df = add_features(df)
    # Save dataset with new features
    df.to_parquet("data/processed/ecommerce_dataset_10000_cleaned.parquet", index=False)
    print("Features added successfully.")
