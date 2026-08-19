import pandas as pd
import os

DATA_DIR = r"D:\sales_data_warehouse_project\data\raw"

files = {
    "superstore": "superstore.csv",
    "online_retail": "online_retail.csv",
    "adventureworks": "adventureworks.csv",
}

for name, filename in files.items():
    filepath = os.path.join(DATA_DIR, filename)
    print("=" * 60)
    print(f"DATASET: {name.upper()}")
    print("=" * 60)

    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn Names:\n{list(df.columns)}")

    print(f"\nData Types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")

    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    for col in df.columns:
        if missing[col] > 0:
            pct = (missing[col] / len(df)) * 100
            print(f"  {col}: {missing[col]:,} ({pct:.1f}%)")
    if missing.sum() == 0:
        print("  None")

    print(f"\nDuplicate Rows: {df.duplicated().sum():,}")

    print(f"\nKey Column Unique Values:")
    for col in df.columns:
        if "id" in col.lower() or "key" in col.lower() or "number" in col.lower() or "no" in col.lower():
            print(f"  {col}: {df[col].nunique():,} unique")

    date_cols = [col for col in df.columns if "date" in col.lower()]
    if date_cols:
        print(f"\nDate Range:")
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"  {col}: {df[col].min()} to {df[col].max()}")

    qty_cols = [col for col in df.columns if "quantity" in col.lower() or "qty" in col.lower()]
    if qty_cols:
        print(f"\nQuantity Check:")
        for col in qty_cols:
            neg = (df[col] < 0).sum()
            zero = (df[col] == 0).sum()
            print(f"  {col}: min={df[col].min()}, max={df[col].max()}, negatives={neg:,}, zeros={zero:,}")

    price_cols = [col for col in df.columns if "price" in col.lower() or "sales" in col.lower() or "amount" in col.lower() or "total" in col.lower()]
    if price_cols:
        print(f"\nPrice/Sales Check:")
        for col in price_cols:
            neg = (df[col] < 0).sum()
            zero = (df[col] == 0).sum()
            print(f"  {col}: min={df[col].min()}, max={df[col].max()}, negatives={neg:,}, zeros={zero:,}")

    print("\n")