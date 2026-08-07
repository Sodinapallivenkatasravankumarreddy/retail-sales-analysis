"""
generate_data.py
Generates a realistic synthetic retail sales dataset for analysis.
Run: python scripts/generate_data.py
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# --- Config ---
N_ROWS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

CATEGORIES = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Tablet"],
    "Home & Kitchen": ["Blender", "Air Fryer", "Coffee Maker", "Cookware Set", "Vacuum"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Beauty": ["Moisturizer", "Shampoo", "Perfume", "Lipstick", "Sunscreen"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Bicycle", "Tent"],
}

REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Online", "In-Store"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash", "Wallet"]

BASE_PRICES = {
    "Headphones": 49, "Smartphone": 699, "Laptop": 999, "Smartwatch": 199, "Tablet": 349,
    "Blender": 39, "Air Fryer": 89, "Coffee Maker": 59, "Cookware Set": 129, "Vacuum": 149,
    "T-Shirt": 15, "Jeans": 45, "Jacket": 89, "Sneakers": 65, "Dress": 55,
    "Moisturizer": 22, "Shampoo": 12, "Perfume": 65, "Lipstick": 18, "Sunscreen": 16,
    "Yoga Mat": 25, "Dumbbells": 45, "Running Shoes": 79, "Bicycle": 349, "Tent": 129,
}


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=np.random.randint(0, delta.days), seconds=np.random.randint(0, 86400))


rows = []
for i in range(N_ROWS):
    category = np.random.choice(list(CATEGORIES.keys()))
    product = np.random.choice(CATEGORIES[category])
    base_price = BASE_PRICES[product]

    # seasonal + random noise on price (discounts etc.)
    date = random_date(START_DATE, END_DATE)
    month = date.month
    seasonal_boost = 1.3 if month in (11, 12) else 1.0  # holiday season boost
    discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.5, 0.2, 0.15, 0.1, 0.05])
    unit_price = round(base_price * (1 - discount), 2)

    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.2, 0.1, 0.15, 0.08, 0.06, 0.04, 0.02])
    quantity = int(quantity * seasonal_boost) if seasonal_boost > 1 and np.random.rand() < 0.4 else quantity
    quantity = max(1, quantity)

    revenue = round(unit_price * quantity, 2)
    region = np.random.choice(REGIONS)
    channel = np.random.choice(CHANNELS, p=[0.62, 0.38])
    payment = np.random.choice(PAYMENT_METHODS, p=[0.35, 0.25, 0.2, 0.1, 0.1])
    customer_age = int(np.clip(np.random.normal(34, 12), 18, 75))
    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.07, 0.15, 0.35, 0.40])

    rows.append({
        "order_id": f"ORD{100000 + i}",
        "order_date": date.strftime("%Y-%m-%d"),
        "category": category,
        "product": product,
        "unit_price": unit_price,
        "quantity": quantity,
        "revenue": revenue,
        "discount_pct": discount,
        "region": region,
        "sales_channel": channel,
        "payment_method": payment,
        "customer_age": customer_age,
        "customer_rating": rating,
    })

df = pd.DataFrame(rows).sort_values("order_date").reset_index(drop=True)

# Inject a few realistic data-quality issues for cleaning practice
dupe_rows = df.sample(15, random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

missing_idx = df.sample(40, random_state=2).index
df.loc[missing_idx, "customer_rating"] = np.nan

missing_age_idx = df.sample(25, random_state=3).index
df.loc[missing_age_idx, "customer_age"] = np.nan

df.to_csv("data/retail_sales.csv", index=False)
print(f"Generated {len(df)} rows -> data/retail_sales.csv")
