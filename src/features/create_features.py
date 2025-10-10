name: Feature Engineering & Dataset Preparation

on:
  push:
    branches:
      - main
    paths:
      - "data/raw/**"           # Only trigger if raw dataset or metadata changed
      - "src/features/**"
      - "src/data/**"
  workflow_dispatch:            # Allow manual execution from Actions tab

jobs:
  feature-engineering:
    runs-on: ubuntu-latest

    steps:
      - name: ✅ Checkout repository
        uses: actions/checkout@v3

      - name: 🐍 Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 📦 Install required dependencies
        run: |
          pip install -r requirements.txt

      - name: 🔍 Check raw dataset existence
        run: |
          if [ ! -f "data/raw/dataset-metadata.json" ]; then
            echo "❌ Raw dataset metadata not found. Skipping feature engineering."
            exit 1
          else
            echo "✅ Raw dataset metadata found."
          fi

      - name: 🚀 Running Feature Engineering (create_features.py)
        run: |
          echo "Running Feature Engineering pipeline..."
          python src/features/create_features.py

      - name: 📁 Verify generated files
        run: |
          echo "🔍 Checking processed outputs..."
          ls -lh data/processed || echo "⚠ No processed directory found."
          if [ -f "data/processed/ecommerce_dataset_10000_cleaned.csv" ]; then
            echo "✅ CSV successfully generated."
          else
            echo "❌ CSV missing - check your script."
            exit 1
          fi
          if [ -f "data/processed/ecommerce_dataset_10000_cleaned.parquet" ]; then
            echo "✅ Parquet successfully generated."
          else
            echo "⚠ Parquet missing - but CSV exists, so dashboard will still work."
          fi

      - name: 💾 Commit processed dataset updates (if any)
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/processed/
          if git diff --staged --quiet; then
            echo "ℹ️ No changes to commit in processed data."
          else
            git commit -m "feat: automated feature engineering output update"
            git push origin main
            echo "✅ Processed dataset updated and committed."
          fi
