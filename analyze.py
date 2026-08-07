"""
analyze.py
End-to-end analysis of retail_sales.csv:
 1. Load & clean data
 2. Compute key business metrics
 3. Generate charts into /visuals
 4. Print a summary report to console

Run: python scripts/analyze.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.width", 120)

# ---------------------------------------------------------------
# 1. LOAD & CLEAN
# ---------------------------------------------------------------
df = pd.read_csv("data/retail_sales.csv", parse_dates=["order_date"])

print("=" * 60)
print("STEP 1: DATA CLEANING")
print("=" * 60)
print(f"Raw rows: {len(df)}")

dupes = df.duplicated(subset=["order_id"]).sum()
df = df.drop_duplicates(subset=["order_id"])
print(f"Removed {dupes} duplicate order_ids")

missing_before = df.isna().sum()
print("\nMissing values before fill:")
print(missing_before[missing_before > 0])

df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())
df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())

df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df["order_year"] = df["order_date"].dt.year
df["day_of_week"] = df["order_date"].dt.day_name()

print(f"\nClean rows: {len(df)}")

# ---------------------------------------------------------------
# 2. KEY METRICS
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2: KEY BUSINESS METRICS")
print("=" * 60)

total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = df.groupby("order_id")["revenue"].sum().mean()
avg_rating = df["customer_rating"].mean()

print(f"Total Revenue:      ${total_revenue:,.2f}")
print(f"Total Orders:       {total_orders:,}")
print(f"Avg Order Value:    ${avg_order_value:,.2f}")
print(f"Avg Customer Rating:{avg_rating:.2f} / 5")

top_category = df.groupby("category")["revenue"].sum().idxmax()
top_product = df.groupby("product")["revenue"].sum().idxmax()
top_region = df.groupby("region")["revenue"].sum().idxmax()

print(f"\nTop Category:       {top_category}")
print(f"Top Product:         {top_product}")
print(f"Top Region:          {top_region}")

# ---------------------------------------------------------------
# 3. VISUALS
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 3: GENERATING CHARTS -> /visuals")
print("=" * 60)

# 3.1 Monthly revenue trend
monthly = df.groupby("order_month")["revenue"].sum().reset_index()
plt.figure(figsize=(11, 5))
sns.lineplot(data=monthly, x="order_month", y="revenue", marker="o", color="#2563eb")
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
plt.ylabel("Revenue ($)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("visuals/01_monthly_revenue_trend.png", dpi=150)
plt.close()

# 3.2 Revenue by category
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(9, 5))
sns.barplot(data=cat_rev, x="revenue", y="category", hue="category", palette="Blues_d", legend=False)
plt.title("Revenue by Category", fontsize=14, fontweight="bold")
plt.xlabel("Revenue ($)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("visuals/02_revenue_by_category.png", dpi=150)
plt.close()

# 3.3 Sales channel split
channel_rev = df.groupby("sales_channel")["revenue"].sum()
plt.figure(figsize=(6, 6))
plt.pie(channel_rev, labels=channel_rev.index, autopct="%1.1f%%",
        colors=["#2563eb", "#93c5fd"], startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2})
plt.title("Revenue Share by Sales Channel", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("visuals/03_channel_split.png", dpi=150)
plt.close()

# 3.4 Revenue by region
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=region_rev, x="region", y="revenue", hue="region", palette="Greens_d", legend=False)
plt.title("Revenue by Region", fontsize=14, fontweight="bold")
plt.ylabel("Revenue ($)")
plt.xlabel("")
plt.tight_layout()
plt.savefig("visuals/04_revenue_by_region.png", dpi=150)
plt.close()

# 3.5 Customer age distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["customer_age"], bins=20, color="#7c3aed", kde=True)
plt.title("Customer Age Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Age")
plt.tight_layout()
plt.savefig("visuals/05_customer_age_distribution.png", dpi=150)
plt.close()

# 3.6 Day-of-week order pattern
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_rev = df.groupby("day_of_week")["revenue"].sum().reindex(dow_order).reset_index()
plt.figure(figsize=(9, 5))
sns.barplot(data=dow_rev, x="day_of_week", y="revenue", hue="day_of_week", palette="Oranges_d", legend=False)
plt.title("Revenue by Day of Week", fontsize=14, fontweight="bold")
plt.ylabel("Revenue ($)")
plt.xlabel("")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("visuals/06_revenue_by_day_of_week.png", dpi=150)
plt.close()

print("Saved 6 charts to /visuals")

# ---------------------------------------------------------------
# 4. EXPORT CLEAN DATA + SUMMARY
# ---------------------------------------------------------------
df.to_csv("data/retail_sales_clean.csv", index=False)

summary = pd.DataFrame({
    "metric": ["total_revenue", "total_orders", "avg_order_value", "avg_rating",
               "top_category", "top_product", "top_region"],
    "value": [total_revenue, total_orders, round(avg_order_value, 2), round(avg_rating, 2),
              top_category, top_product, top_region]
})
summary.to_csv("data/summary_metrics.csv", index=False)

print("\nSaved cleaned data -> data/retail_sales_clean.csv")
print("Saved summary metrics -> data/summary_metrics.csv")
print("\nDone.")
