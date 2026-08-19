import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

DATA_DIR = r"D:\sales_data_warehouse_project\data\raw"


def load_superstore():
    filepath = os.path.join(DATA_DIR, "superstore.csv")
    df = pd.read_csv(filepath, encoding="latin-1")
    df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]
    df["source_system"] = "superstore"
    df = df.where(pd.notnull(df), None)
    df.to_sql("superstore_sales", engine, schema="raw", if_exists="replace", index=False)
    print(f"Superstore: {len(df)} rows loaded")


def load_online_retail():
    filepath = os.path.join(DATA_DIR, "online_retail.csv")
    df = pd.read_csv(filepath, encoding="latin-1")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.rename(columns={
        "invoiceno": "invoice_no",
        "stockcode": "stock_code",
        "invoicedate": "invoice_date",
        "unitprice": "unit_price",
        "customerid": "customer_id"
    })
    df["source_system"] = "online_retail"
    df["customer_id"] = df["customer_id"].astype("Int64").astype(str)
    df["customer_id"] = df["customer_id"].replace("<NA>", None)
    df = df.where(pd.notnull(df), None)
    df.to_sql("online_retail", engine, schema="raw", if_exists="replace", index=False)
    print(f"Online Retail: {len(df)} rows loaded")


def load_adventureworks():
    filepath = os.path.join(DATA_DIR, "adventureworks.csv")
    df = pd.read_csv(filepath, encoding="latin-1")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df["source_system"] = "adventureworks"
    df = df.where(pd.notnull(df), None)
    df.to_sql("adventureworks_sales", engine, schema="raw", if_exists="replace", index=False)
    print(f"AdventureWorks: {len(df)} rows loaded")


if __name__ == "__main__":
    print("Starting ETL pipeline...")
    load_superstore()
    load_online_retail()
    load_adventureworks()
    print("ETL pipeline complete!")