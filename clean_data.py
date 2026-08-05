"""
Standalone cleaning script — takes data/raw_orders.csv and produces:
  - data/cleaned_orders.csv   (full cleaned dataset, all statuses)
  - data/orders_powerbi.csv   (completed orders only, ready for Power BI import)
  - data/retail.db            (SQLite DB with a `orders` table, for SQL practice)

Run: python clean_data.py
"""
import pandas as pd
import numpy as np
import sqlite3
import os

RAW_PATH = "data/raw_orders.csv"


def parse_mixed_date(val):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT


def cap_outliers(s):
    cap = s.quantile(0.99) * 5
    median = s.median()
    return s.mask(s > cap, median)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.copy()
    clean = clean.drop_duplicates()

    text_cols = ["country", "payment_method", "channel", "order_status", "category"]
    for col in text_cols:
        clean[col] = clean[col].astype(str).str.strip().str.title()
        clean.loc[clean[col].isin(["Nan", "None"]), col] = np.nan

    clean["country"] = clean["country"].replace({"Usa": "United States", "Uk": "United Kingdom"})
    clean["order_date"] = clean["order_date"].apply(parse_mixed_date)
    clean["customer_id"] = clean["customer_id"].fillna("UNKNOWN")

    clean["unit_price"] = clean.groupby("category")["unit_price"].transform(lambda s: s.fillna(s.median()))
    clean["quantity"] = clean["quantity"].fillna(1)
    clean["unit_price"] = clean.groupby("category")["unit_price"].transform(cap_outliers)
    clean["payment_method"] = clean["payment_method"].fillna("Unknown")
    clean = clean.dropna(subset=["order_date"])

    clean["revenue"] = clean["unit_price"] * clean["quantity"]
    clean["order_date"] = clean["order_date"].dt.date.astype(str)  # SQLite/Power BI friendly
    clean["month"] = pd.to_datetime(clean["order_date"]).dt.strftime("%Y-%m")
    clean["quarter"] = pd.to_datetime(clean["order_date"]).dt.quarter
    clean["year"] = pd.to_datetime(clean["order_date"]).dt.year

    return clean


def main():
    df = pd.read_csv(RAW_PATH)
    clean = clean_orders(df)

    os.makedirs("data", exist_ok=True)
    clean.to_csv("data/cleaned_orders.csv", index=False)

    completed = clean[clean["order_status"].isin(["Delivered", "Returned"])]
    completed.to_csv("data/orders_powerbi.csv", index=False)

    conn = sqlite3.connect("data/retail.db")
    clean.to_sql("orders", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Cleaned rows: {len(clean)}  |  Completed (Power BI export): {len(completed)}")
    print("Wrote data/cleaned_orders.csv, data/orders_powerbi.csv, data/retail.db")


if __name__ == "__main__":
    main()
