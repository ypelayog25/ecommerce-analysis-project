import pandas as pd

def load_dataset(path="data/processed/ecommerce_dataset_10000_cleaned.parquet"):
    """
    Load the cleaned parquet dataset.
    """
    df = pd.read_parquet(path)
    return df

if __name__ == "__main__":
    # Load dataset and print shape
    df = load_dataset()
    print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
