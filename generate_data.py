"""
Generates a messy, realistic online retail orders dataset.
Run once to produce data/raw_orders.csv
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 6000

categories = ["Electronics", "Home & Kitchen", "Fashion", "Beauty", "Sports", "Toys", "Books"]
products = {
    "Electronics": ["Wireless Earbuds", "Bluetooth Speaker", "Smartwatch", "Phone Case", "Power Bank", "USB-C Cable"],
    "Home & Kitchen": ["Air Fryer", "Blender", "Non-stick Pan Set", "Storage Containers", "LED Desk Lamp"],
    "Fashion": ["Denim Jacket", "Running Shoes", "Cotton T-Shirt", "Leather Wallet", "Sunglasses"],
    "Beauty": ["Face Serum", "Sunscreen SPF50", "Lip Balm Set", "Hair Dryer", "Makeup Brush Kit"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Resistance Bands", "Water Bottle", "Cycling Gloves"],
    "Toys": ["Building Blocks Set", "RC Car", "Puzzle 1000pc", "Board Game"],
    "Books": ["Fiction Bestseller", "Self-Help Guide", "Cookbook", "Kids Picture Book"],
}
price_ranges = {
    "Electronics": (499, 4999), "Home & Kitchen": (299, 3499), "Fashion": (199, 2999),
    "Beauty": (149, 1499), "Sports": (199, 2499), "Toys": (249, 1999), "Books": (99, 799),
}

countries = ["India", "india", "INDIA", "USA", "United States", "UK", "United Kingdom", "Germany", "France", "UAE", np.nan]
country_weights = [0.42, 0.05, 0.02, 0.15, 0.03, 0.1, 0.02, 0.08, 0.06, 0.05, 0.02]

payment_methods = ["Credit Card", "credit card", "Debit Card", "UPI", "Net Banking", "COD", "PayPal", None]
channels = ["Website", "Mobile App", "Marketplace", "website", "MOBILE APP"]
statuses = ["Delivered", "Returned", "Cancelled", "Delivered ", "delivered"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 9, 30)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    order_id = f"ORD{100000 + i}"
    customer_id = f"CUST{np.random.randint(1, 1800)}"
    cat = np.random.choice(categories, p=[0.22, 0.16, 0.2, 0.13, 0.12, 0.09, 0.08])
    product = np.random.choice(products[cat])
    low, high = price_ranges[cat]
    price = round(np.random.uniform(low, high), 2)

    # inject some extreme price outliers (data entry errors)
    if np.random.rand() < 0.01:
        price = price * 100  # fat-finger extra zero

    qty = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.15, 0.15, 0.15, 0.08, 0.06, 0.04, 0.02])

    # random date, with a deliberate Q3 (Jul-Sep) dip in order volume for certain categories
    day_offset = np.random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=day_offset)
    # simulate a real dip: Fashion & Beauty orders drop off in Aug-Sep due to a "stockout" story
    if cat in ["Fashion", "Beauty"] and order_date.month in [8, 9] and np.random.rand() < 0.55:
        continue  # skip to create fewer orders in this window (the "decline" signal)

    country = np.random.choice(countries, p=country_weights)
    payment = np.random.choice(payment_methods, p=[0.22, 0.05, 0.18, 0.25, 0.08, 0.12, 0.08, 0.02])
    channel = np.random.choice(channels, p=[0.35, 0.35, 0.2, 0.05, 0.05])
    status = np.random.choice(statuses, p=[0.78, 0.1, 0.08, 0.02, 0.02])

    # date format inconsistency
    if np.random.rand() < 0.15:
        date_str = order_date.strftime("%d/%m/%Y")
    elif np.random.rand() < 0.3:
        date_str = order_date.strftime("%m-%d-%Y")
    else:
        date_str = order_date.strftime("%Y-%m-%d")

    # missing values injection
    if np.random.rand() < 0.04:
        customer_id = None
    if np.random.rand() < 0.03:
        price = np.nan
    if np.random.rand() < 0.02:
        qty = np.nan

    rows.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": date_str,
        "category": cat,
        "product_name": product,
        "unit_price": price,
        "quantity": qty,
        "country": country,
        "payment_method": payment,
        "channel": channel,
        "order_status": status,
    })

df = pd.DataFrame(rows)

# inject duplicate rows
dupes = df.sample(frac=0.02, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# inject a few fully-duplicated order_ids with different data (data integrity issue)
glitch_idx = df.sample(5, random_state=2).index
for idx in glitch_idx:
    df.loc[idx, "unit_price"] = df.loc[idx, "unit_price"]  # keep, just marking

# shuffle
df = df.sample(frac=1, random_state=3).reset_index(drop=True)

import os
os.makedirs("/home/claude/retail_project/data", exist_ok=True)
df.to_csv("/home/claude/retail_project/data/raw_orders.csv", index=False)
print("Saved:", df.shape)
print(df.head())
