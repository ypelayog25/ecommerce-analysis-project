name: Feature Engineering - Generate Enhanced Dataset (Parquet + CSV)

on:
  schedule:
    - cron: "15 1 * * *" # Ejecutar todos los días a la 01:15 UTC (no coincide con update_dataset)
  workflow_dispatch:

jobs:
  feature-engineering:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pandas pyarrow

      - name: Ensure Python module paths (__init__.py + PYTHONPATH)
        run: |
          touch src/__init__.py
          touch src/data/__init__.py
          touch src/features/__init__.py
          touch src/models/__init__.py
          touch src/visualization/__init__.py
          echo "PYTHONPATH=$PWD" >> $GITHUB_ENV
          echo "✅ Python package structure ensured"

      - name: Check dataset hash before running
        id: hash-check
        run: |
          DATASET="data/processed/ecommerce_dataset_10000_cleaned.parquet"
          HASH_FILE="data/processed/.feature_hash.txt"
          if [ ! -f "$DATASET" ]; then
            echo "❌ Dataset base no encontrado: $DATASET"
            exit 1
          fi
          NEW_HASH=$(sha256sum "$DATASET" | cut -d " " -f1)
          if [ -f "$HASH_FILE" ]; then
            OLD_HASH=$(cat "$HASH_FILE")
          else
            OLD_HASH=""
          fi
          echo "OLD_HASH=$OLD_HASH"
          echo "NEW_HASH=$NEW_HASH"
          if [[ "$NEW_HASH" != "$OLD_HASH" ]]; then
            echo "✅ Cambios detectados, ejecutando feature engineering"
            echo "changed=true" >> $GITHUB_OUTPUT
          else
            echo "ℹ️ No hay cambios en el dataset base — se omite procesamiento"
            echo "changed=false" >> $GITHUB_OUTPUT
          fi

      - name: Run Feature Engineering (create_features.py)
        if: steps.hash-check.outputs.changed == 'true'
        run: |
          echo "🚀 Running: src/features/create_features.py"
          python src/features/create_features.py

      - name: Export processed dataset (Parquet + CSV)
        if: steps.hash-check.outputs.changed == 'true'
        run: |
          echo "📦 Exporting datasets..."
          python - <<EOF
          import pandas as pd
          df = pd.read_parquet("data/processed/ecommerce_dataset_features.parquet")
          df.to_csv("data/processed/ecommerce_dataset_features.csv", index=False)
          print("✅ CSV generated")
          EOF

      - name: Save new dataset hash
        if: steps.hash-check.outputs.changed == 'true'
        run: |
          NEW_HASH=$(sha256sum data/processed/ecommerce_dataset_10000_cleaned.parquet | cut -d " " -f1)
          echo "$NEW_HASH" > data/processed/.feature_hash.txt

      - name: Commit and push changes in a new branch
        if: steps.hash-check.outputs.changed == 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCH_NAME=auto/features-$(date +'%Y%m%d%H%M%S')
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git checkout -b $BRANCH_NAME
          git add data/processed/ecommerce_dataset_features.parquet data/processed/ecommerce_dataset_features.csv data/processed/.feature_hash.txt
          git commit -m "feat: updated feature dataset"
          git push --set-upstream origin $BRANCH_NAME

      - name: Create Pull Request and Tag Version
        if: steps.hash-check.outputs.changed == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
          base: main
          title: "🚀 Update Feature Dataset"
          body: "Auto-generated updated feature dataset with Parquet + CSV export."
          labels: feature, automation
