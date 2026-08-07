# 🛍️ Retail Sales Analysis

An end-to-end data analysis project exploring two years of retail sales data — from raw data cleaning through business insights and visualizations. Built as a data analyst portfolio piece.

## 📌 Project Overview

This project simulates a real-world data analyst workflow:

1. **Data generation** — a realistic synthetic retail sales dataset (5,000+ transactions, with intentional duplicates and missing values to practice cleaning)
2. **Data cleaning** — deduplication, missing-value imputation, feature engineering (month, year, day-of-week)
3. **Exploratory analysis** — revenue trends, category/region/channel breakdowns, customer demographics
4. **Visualization** — six publication-ready charts
5. **Reporting** — key metrics exported for dashboarding or stakeholder review

## 📊 Key Insights

| Metric | Value |
|---|---|
| Total Revenue | $1,143,469.90 |
| Total Orders | 5,000 |
| Average Order Value | $228.69 |
| Average Customer Rating | 4.04 / 5 |
| Top Category | Electronics |
| Top Product | Laptop |
| Top Region | Central |

**Highlights:**
- Revenue peaks sharply in **Nov–Dec 2025**, consistent with holiday-season seasonality built into the model.
- **Electronics** drives the largest share of revenue, led by laptops and smartphones.
- **Online** sales channel outperforms in-store, though the split is closer than typical e-commerce benchmarks — a signal worth digging into with real data.
- The **Central** region leads in total revenue, suggesting a potential focus area for expansion or inventory prioritization.

## 📁 Project Structure

```
retail-sales-analysis/
├── data/
│   ├── retail_sales.csv          # Raw generated dataset
│   ├── retail_sales_clean.csv    # Cleaned dataset (output)
│   └── summary_metrics.csv       # Key metrics summary (output)
├── scripts/
│   ├── generate_data.py          # Generates the synthetic dataset
│   └── analyze.py                # Cleans data, computes metrics, builds charts
├── visuals/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_revenue_by_category.png
│   ├── 03_channel_split.png
│   ├── 04_revenue_by_region.png
│   ├── 05_customer_age_distribution.png
│   └── 06_revenue_by_day_of_week.png
├── requirements.txt
└── README.md
```

## 🖼️ Sample Visuals

**Monthly Revenue Trend**
![Monthly Revenue Trend](visuals/01_monthly_revenue_trend.png)

**Revenue by Category**
![Revenue by Category](visuals/02_revenue_by_category.png)

## 🛠️ Tech Stack

- **Python 3** — pandas, numpy for data wrangling
- **Matplotlib & Seaborn** — visualization
- **CSV** — lightweight, portable data storage (easily swapped for a real SQL source)

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/retail-sales-analysis.git
cd retail-sales-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python scripts/generate_data.py

# 4. Run the analysis
python scripts/analyze.py
```

Charts will be saved to `/visuals`, and cleaned data + summary metrics to `/data`.

## 🔎 Possible Extensions

- Swap the CSV pipeline for a real SQL database (PostgreSQL / SQLite) and rewrite metrics as SQL queries
- Build an interactive dashboard with Plotly Dash, Streamlit, or Power BI / Tableau
- Add cohort or RFM (Recency, Frequency, Monetary) customer segmentation
- A/B test simulated pricing or promotion strategies

## 📄 License

MIT — feel free to fork and adapt for your own portfolio.
