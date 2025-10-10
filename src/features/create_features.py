import pandas as pd

def add_features(df):
    # Calculate revenue for each order
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    # Extract order month from OrderDate
    df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.to_period('M')
    return df

if __name__ == "__main__":
    # Load cleaned dataset
    df = pd.read_parquet("data/processed/ecommerce_dataset_10000_cleaned.parquet")
    # Add calculated features
    df = add_features(df)
    # Save the updated dataset
    df.to_parquet("data/processed/ecommerce_dataset_10000_cleaned.parquet", index=False)
    print("Features added successfully.")
