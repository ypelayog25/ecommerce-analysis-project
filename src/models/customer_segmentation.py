import pandas as pd
from sklearn.cluster import KMeans
from src.data.load_dataset import load_dataset

def segment_customers(df, n_clusters=4):
    """
    Segment customers based on Revenue and Quantity.
    """
    customer_summary = df.groupby('CustomerID').agg({
        'Revenue':'sum',
        'Quantity':'sum'
    }).reset_index()

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    customer_summary['Segment'] = kmeans.fit_predict(customer_summary[['Revenue','Quantity']])
    return customer_summary

if __name__ == "__main__":
    df = load_dataset()
    segments = segment_customers(df)
    segments.to_csv("data/processed/customer_segments.csv", index=False)
    print("Customer segmentation completed.")
