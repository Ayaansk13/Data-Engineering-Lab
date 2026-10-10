"""
========================================================================================
PRACTICAL-10: END-TO-END RETAIL DATA ENGINEERING PLATFORM & DATA WAREHOUSE (MINI PROJECT)
========================================================================================
Course: Data Engineering
Author:
  Name: Mohammad Ayaan Sajid Shaikh
  Roll No.: 47
  Student ID: 5135870

Components:
  1. Data Ingestion (Heterogeneous Sources: CSV, JSON, Web Logs)
  2. Data Quality & Cleaning (Silver Layer Quarantine Architecture)
  3. Transformation & Feature Engineering (RFM Customer Segmentation)
  4. Data Warehouse Design (Star Schema in SQLite with Analytical Data Marts)
  5. Executive Reporting & Visual Analytics
========================================================================================
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_SILVER = os.path.join(BASE_DIR, "data", "silver")
DATA_GOLD = os.path.join(BASE_DIR, "data", "gold")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

for d in [DATA_RAW, DATA_SILVER, DATA_GOLD, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)


def run_pipeline():
    print("=" * 80)
    print("STARTING END-TO-END DATA ENGINEERING PIPELINE")
    print("Author: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)")
    print("=" * 80)

    # 1. INGESTION
    print("\n[STAGE 1] Ingesting Raw Data Sources...")
    customers_raw = pd.read_csv(os.path.join(DATA_RAW, "customers.csv"))
    with open(os.path.join(DATA_RAW, "products.json"), "r") as f:
        products_raw = pd.DataFrame(json.load(f))
    transactions_raw = pd.read_csv(os.path.join(DATA_RAW, "transactions.csv"))
    with open(os.path.join(DATA_RAW, "web_logs.json"), "r") as f:
        web_logs_raw = pd.DataFrame(json.load(f))

    print(f"  ✓ Ingested customers.csv:     {len(customers_raw)} records")
    print(f"  ✓ Ingested products.json:      {len(products_raw)} records")
    print(f"  ✓ Ingested transactions.csv:  {len(transactions_raw)} records")
    print(f"  ✓ Ingested web_logs.json:      {len(web_logs_raw)} records")

    # 2. DATA QUALITY & SILVER LAYER
    print("\n[STAGE 2] Executing Data Quality Rules & Quarantine Logic...")
    rejected_records = []

    # Clean Customers
    c_clean = customers_raw.drop_duplicates(subset=["customer_id"], keep="first").copy()
    c_clean["city"] = c_clean["city"].str.strip().str.title()
    c_clean["email"] = c_clean["email"].fillna("unregistered@example.com")

    # Clean Products
    valid_products = []
    for _, row in products_raw.iterrows():
        if pd.isna(row["category"]) or row["unit_cost"] <= 0 or row["unit_price"] <= 0:
            rejected_records.append({
                "record_type": "Product",
                "identifier": str(row["product_id"]),
                "reason": "Invalid category or non-positive financial values",
                "raw_data": str(row.to_dict())
            })
        else:
            valid_products.append(row)
    p_clean = pd.DataFrame(valid_products)

    # Clean Transactions
    valid_cust_ids = set(c_clean["customer_id"])
    valid_prod_ids = set(p_clean["product_id"])
    t_dedup = transactions_raw.drop_duplicates(subset=["order_id"], keep="first").copy()
    clean_txs = []

    for _, row in t_dedup.iterrows():
        order_id = row["order_id"]
        cid = row["customer_id"]
        pid = row["product_id"]
        qty = row["quantity"]
        dt_str = str(row["order_date"])

        try:
            order_dt = pd.to_datetime(dt_str)
        except Exception:
            order_dt = pd.NaT

        if pd.isna(order_dt):
            rejected_records.append({"record_type": "Transaction", "identifier": order_id, "reason": f"Corrupted date: {dt_str}", "raw_data": str(row.to_dict())})
            continue
        if qty <= 0:
            rejected_records.append({"record_type": "Transaction", "identifier": order_id, "reason": f"Non-positive quantity: {qty}", "raw_data": str(row.to_dict())})
            continue
        if cid not in valid_cust_ids:
            rejected_records.append({"record_type": "Transaction", "identifier": order_id, "reason": f"FK Violation: Customer {cid} missing", "raw_data": str(row.to_dict())})
            continue
        if pid not in valid_prod_ids:
            rejected_records.append({"record_type": "Transaction", "identifier": order_id, "reason": f"FK Violation: Product {pid} missing", "raw_data": str(row.to_dict())})
            continue

        row_dict = row.to_dict()
        row_dict["order_date"] = order_dt.strftime("%Y-%m-%d")
        clean_txs.append(row_dict)

    t_clean = pd.DataFrame(clean_txs)
    df_rejected = pd.DataFrame(rejected_records)

    # Save Silver
    c_clean.to_csv(os.path.join(DATA_SILVER, "clean_customers.csv"), index=False)
    p_clean.to_csv(os.path.join(DATA_SILVER, "clean_products.csv"), index=False)
    t_clean.to_csv(os.path.join(DATA_SILVER, "clean_transactions.csv"), index=False)
    df_rejected.to_csv(os.path.join(DATA_SILVER, "quarantine_rejected.csv"), index=False)
    print(f"  ✓ Silver clean tables saved. Quarantined {len(df_rejected)} records.")

    # 3. TRANSFORMATION & RFM
    print("\n[STAGE 3] Transforming & Computing Business Metrics (RFM)...")
    sales = t_clean.merge(p_clean, on="product_id", how="inner")
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    sales["total_cost"] = sales["quantity"] * sales["unit_cost"]
    sales["profit"] = sales["revenue"] - sales["total_cost"]
    sales["profit_margin_pct"] = (sales["profit"] / sales["revenue"]) * 100

    # Customer RFM
    completed = sales[sales["order_status"] == "Completed"].copy()
    completed["order_date_dt"] = pd.to_datetime(completed["order_date"])
    ref_dt = completed["order_date_dt"].max() + pd.Timedelta(days=1)
    rfm = completed.groupby("customer_id").agg(
        recency=("order_date_dt", lambda x: (ref_dt - x.max()).days),
        frequency=("order_id", "count"),
        monetary=("revenue", "sum")
    ).reset_index()

    def seg(r):
        if r["frequency"] >= 8 and r["monetary"] >= 150000:
            return "Champion"
        elif r["frequency"] >= 6:
            return "Loyal Customer"
        elif r["recency"] <= 45:
            return "Potential Loyalist"
        return "At Risk"

    rfm["segment"] = rfm.apply(seg, axis=1)
    c_clean = c_clean.merge(rfm[["customer_id", "segment"]], on="customer_id", how="left")
    c_clean["segment"] = c_clean["segment"].fillna("New / Inactive")

    # 4. DATA WAREHOUSE (STAR SCHEMA)
    print("\n[STAGE 4] Loading Star Schema into Data Warehouse (ecommerce_dwh.db)...")
    dwh_path = os.path.join(DATA_GOLD, "ecommerce_dwh.db")
    if os.path.exists(dwh_path):
        os.remove(dwh_path)
    conn = sqlite3.connect(dwh_path)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE dim_date (
        date_key INTEGER PRIMARY KEY,
        full_date TEXT NOT NULL UNIQUE,
        day_number INTEGER,
        month_number INTEGER,
        month_name TEXT,
        quarter INTEGER,
        year_number INTEGER,
        day_name TEXT,
        is_weekend INTEGER
    );
    CREATE TABLE dim_customer (
        customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT NOT NULL UNIQUE,
        customer_name TEXT NOT NULL,
        email TEXT,
        city TEXT,
        customer_segment TEXT
    );
    CREATE TABLE dim_product (
        product_key INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL UNIQUE,
        product_name TEXT NOT NULL,
        category TEXT,
        unit_cost REAL,
        unit_price REAL
    );
    CREATE TABLE dim_payment (
        payment_key INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_method TEXT NOT NULL,
        order_status TEXT NOT NULL,
        UNIQUE(payment_method, order_status)
    );
    CREATE TABLE fact_sales (
        sales_key INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL UNIQUE,
        date_key INTEGER NOT NULL,
        customer_key INTEGER NOT NULL,
        product_key INTEGER NOT NULL,
        payment_key INTEGER NOT NULL,
        quantity INTEGER,
        unit_price REAL,
        revenue REAL,
        total_cost REAL,
        profit REAL,
        profit_margin_pct REAL,
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
        FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
        FOREIGN KEY (payment_key) REFERENCES dim_payment(payment_key)
    );
    """)

    # Populate Dimensions
    dates = pd.date_range("2024-01-01", "2024-10-31", freq="D")
    date_rows = [(int(d.strftime("%Y%m%d")), d.strftime("%Y-%m-%d"), d.day, d.month, d.strftime("%B"), (d.month-1)//3+1, d.year, d.strftime("%A"), 1 if d.weekday()>=5 else 0) for d in dates]
    cur.executemany("INSERT INTO dim_date VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", date_rows)

    for _, r in c_clean.iterrows():
        cur.execute("INSERT INTO dim_customer (customer_id, customer_name, email, city, customer_segment) VALUES (?, ?, ?, ?, ?)", (r["customer_id"], r["name"], r["email"], r["city"], r["segment"]))
    for _, r in p_clean.iterrows():
        cur.execute("INSERT INTO dim_product (product_id, product_name, category, unit_cost, unit_price) VALUES (?, ?, ?, ?, ?)", (r["product_id"], r["product_name"], r["category"], r["unit_cost"], r["unit_price"]))
    for _, r in sales[["payment_method", "order_status"]].drop_duplicates().iterrows():
        cur.execute("INSERT INTO dim_payment (payment_method, order_status) VALUES (?, ?)", (r["payment_method"], r["order_status"]))
    conn.commit()

    cust_map = dict(cur.execute("SELECT customer_id, customer_key FROM dim_customer").fetchall())
    prod_map = dict(cur.execute("SELECT product_id, product_key FROM dim_product").fetchall())
    pay_map = {(pm, st): pk for pk, pm, st in cur.execute("SELECT payment_key, payment_method, order_status FROM dim_payment").fetchall()}

    fact_rows = []
    for _, r in sales.iterrows():
        dt_key = int(pd.to_datetime(r["order_date"]).strftime("%Y%m%d"))
        fact_rows.append((
            r["order_id"], dt_key, cust_map[r["customer_id"]], prod_map[r["product_id"]],
            pay_map[(r["payment_method"], r["order_status"])], r["quantity"], r["unit_price"],
            r["revenue"], r["total_cost"], r["profit"], r["profit_margin_pct"]
        ))
    cur.executemany("INSERT INTO fact_sales (order_id, date_key, customer_key, product_key, payment_key, quantity, unit_price, revenue, total_cost, profit, profit_margin_pct) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fact_rows)

    # Views
    cur.executescript("""
    CREATE VIEW v_monthly_financials AS
    SELECT d.year_number, d.month_number, d.month_name, COUNT(f.sales_key) AS order_volume, SUM(f.quantity) AS total_units_sold, ROUND(SUM(f.revenue), 2) AS total_revenue, ROUND(SUM(f.profit), 2) AS total_profit, ROUND((SUM(f.profit) / SUM(f.revenue)) * 100, 2) AS profit_margin_pct
    FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key JOIN dim_payment p ON f.payment_key = p.payment_key WHERE p.order_status = 'Completed' GROUP BY d.year_number, d.month_number, d.month_name ORDER BY d.year_number, d.month_number;

    CREATE VIEW v_category_performance AS
    SELECT p.category, COUNT(DISTINCT p.product_id) AS distinct_products, SUM(f.quantity) AS total_quantity, ROUND(SUM(f.revenue), 2) AS category_revenue, ROUND(SUM(f.profit), 2) AS category_profit, ROUND((SUM(f.profit) / SUM(f.revenue)) * 100, 2) AS margin_pct
    FROM fact_sales f JOIN dim_product p ON f.product_key = p.product_key JOIN dim_payment pay ON f.payment_key = pay.payment_key WHERE pay.order_status = 'Completed' GROUP BY p.category ORDER BY category_revenue DESC;

    CREATE VIEW v_regional_sales AS
    SELECT c.city, COUNT(DISTINCT c.customer_id) AS total_customers, COUNT(f.sales_key) AS total_orders, ROUND(SUM(f.revenue), 2) AS total_revenue
    FROM fact_sales f JOIN dim_customer c ON f.customer_key = c.customer_key JOIN dim_payment pay ON f.payment_key = pay.payment_key WHERE pay.order_status = 'Completed' GROUP BY c.city ORDER BY total_revenue DESC;
    """)
    conn.commit()
    print("  ✓ Star Schema & Analytical Views loaded successfully.")

    # 5. VISUAL DASHBOARD
    print("\n[STAGE 5] Generating Executive Reporting Dashboard...")
    df_monthly = pd.read_sql_query("SELECT * FROM v_monthly_financials", conn)
    df_category = pd.read_sql_query("SELECT * FROM v_category_performance", conn)
    df_regional = pd.read_sql_query("SELECT * FROM v_regional_sales", conn)
    df_rfm = pd.read_sql_query("SELECT customer_segment, COUNT(*) AS count FROM dim_customer GROUP BY customer_segment", conn)

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("RETAIL DATA ENGINEERING PLATFORM - EXECUTIVE DASHBOARD\nEngineered by: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)", fontsize=16, fontweight='bold', y=0.98)

    # 1. Trend
    ax1 = axes[0, 0]
    ax1.plot(df_monthly["month_name"], df_monthly["total_revenue"], marker='o', linewidth=2.5, color='#1f77b4', label="Revenue (INR)")
    ax1.plot(df_monthly["month_name"], df_monthly["total_profit"], marker='s', linewidth=2.5, color='#2ca02c', label="Net Profit (INR)")
    ax1.set_title("Monthly Revenue & Profit Trajectory", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Amount (INR)", fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()

    # 2. Category
    ax2 = axes[0, 1]
    bars = ax2.barh(df_category["category"], df_category["category_revenue"], color=['#3b528b', '#21918c', '#5ec962'])
    ax2.set_title("Revenue Contribution by Product Category", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Revenue (INR)", fontsize=10)
    for bar in bars:
        w = bar.get_width()
        ax2.text(w * 0.75, bar.get_y() + bar.get_height()/2, f"INR {w:,.0f}", ha='center', va='center', color='white', fontweight='bold', fontsize=9)

    # 3. RFM
    ax3 = axes[1, 0]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']
    ax3.pie(df_rfm["count"], labels=df_rfm["customer_segment"], autopct='%1.1f%%', startangle=140, colors=colors[:len(df_rfm)], explode=[0.05]*len(df_rfm), shadow=True)
    ax3.set_title("Customer Base RFM Segmentation", fontsize=12, fontweight='bold')

    # 4. Regional
    ax4 = axes[1, 1]
    sns.barplot(data=df_regional, x="total_revenue", y="city", hue="city", legend=False, palette="viridis", ax=ax4)
    ax4.set_title("Geographic Sales Distribution (Revenue by City)", fontsize=12, fontweight='bold')
    ax4.set_xlabel("Revenue (INR)", fontsize=10)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    dash_img_path = os.path.join(REPORTS_DIR, "executive_dashboard.png")
    plt.savefig(dash_img_path, dpi=300)
    plt.close()
    conn.close()

    print(f"  ✓ Dashboard successfully saved to: {dash_img_path}")
    print("\n" + "=" * 80)
    print("PIPELINE EXECUTION COMPLETED")
    print("Author: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()
