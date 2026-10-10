# Practical-09: End-to-End E-Commerce Data Pipeline with Data Quality Auditing and Incremental CDC

---

## 1. Aim
To architect, implement, and validate an enterprise-grade end-to-end data pipeline for an e-commerce ecosystem consisting of multiple normalized relational entities (`customers`, `products`, `orders`, `payments`), incorporating regex validation, multi-rule anomaly rejection, incremental loading (Change Data Capture pattern), and automated business analytics reporting.

---

## 2. Theory

### 2.1 End-to-End Production Data Pipelines
A production data pipeline orchestrates raw data from operational boundary systems into clean, consolidated analytical datamarts:
- **Ingestion:** Consuming raw transactional streams and flat batch snapshots.
- **Cleansing & Standardizing:** Stripping formatting inconsistencies, standardizing email formats via regex, and casing city names uniformly.
- **Relational Integrity Enforcement:** Defining database schemas with Primary Keys and Foreign Key dependencies (`PRAGMA foreign_keys = ON`) to ensure orphaned records cannot exist.

### 2.2 Incremental Loading & Change Data Capture (CDC)
Full warehouse reloads are computationally expensive and impractical for large datasets:
- **Baseline Batch:** The initial historical load populates the warehouse baseline.
- **Delta Batch:** Periodically arriving files contain a mix of new transactions and potentially repeated records.
- **Idempotent Ingestion:** The pipeline inspects target warehouse tables and inserts *only* rows whose primary keys are not currently present:
  $$\text{Delta Rows} = \text{Incoming} \setminus \text{Existing}$$
This prevents duplicate primary key constraint violations while enabling continuous ingestion.

### 2.3 Automated Business Intelligence Reporting
Once the warehouse tables are populated, automated analytical SQL queries calculate executive key performance indicators (KPIs), such as revenue by city and category, payment fulfillment ratios, and customer spending summaries.

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Libraries:** `pandas`, `sqlite3`, `re`, `os`
- **Environment:** Jupyter Notebook / Local Shell

---

## 4. Procedure
1. **Initialize Source Data:** Generate 8 modular source CSV files split across two distinct phases:
   - Historical Baseline: `customers_historical.csv`, `products_historical.csv`, `orders_historical.csv`, `payments_historical.csv`.
   - Incremental Influx: `customers_new.csv`, `products_new.csv`, `orders_new.csv`, `payments_new.csv`.
2. **Schema Creation:** Initialize SQLite database `ecommerce.db` with normalized tables:
   - `customers`: `customer_id` (PK), `name`, `email`, `city`.
   - `products`: `product_id` (PK), `product_name`, `category`, `price`.
   - `orders`: `order_id` (PK), `customer_id` (FK), `product_id` (FK), `order_date`, `quantity`.
   - `payments`: `payment_id` (PK), `order_id` (FK), `amount`, `status`, `payment_method`.
3. **Task 1: End-to-End Pipeline Execution:**
   - Extract raw files into Pandas DataFrames.
   - Clean data: strip text whitespace, lowercase emails, title-case customer names.
   - Run quality validation: reject invalid emails (regex), non-positive amounts, or missing mandatory fields.
   - Incrementally load valid entities into the database.
4. **Task 2: Relational Verification:** Inspect table schemas, verify foreign key relationships, and query table row counts.
5. **Task 3: Delta Ingestion & CDC:** Ingest newly arriving batch files, filter out existing keys, append genuine delta records, and log rejected rows.
6. **Task 4: Analytical Reporting:** Execute multi-table SQL queries to report revenue by city, category breakdown, and customer order metrics.

---

## 5. Code Explanation

### Multi-Rule Validation Engine
```python
def split_valid(df, checks):
    """Applies a suite of boolean conditions and tags rejection reasons."""
    reasons = pd.Series("", index=df.index, dtype=object)
    for mask, text in checks:
        mask = pd.Series(mask, index=df.index).fillna(False).astype(bool)
        for i in df.index[mask]:
            reasons[i] = (reasons[i] + "; " if reasons[i] else "") + text
            
    valid = df[reasons == ""].copy()
    rejected = df[reasons != ""].copy()
    rejected["reason"] = reasons[reasons != ""]
    return valid, rejected
```

### CDC Incremental Loader
```python
def incremental_load(df, table, key):
    """Inserts only rows whose primary key is absent from the target table."""
    conn = sqlite3.connect("ecommerce.db")
    conn.execute("PRAGMA foreign_keys = ON")
    existing_keys = set(pd.read_sql(f"SELECT {key} FROM {table}", conn)[key])
    
    # Filter delta rows
    delta_df = df[~df[key].isin(existing_keys)]
    if not delta_df.empty:
        delta_df.to_sql(table, conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
```

### Analytical SQL Query
```python
report_query = """
SELECT c.city, p.category,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(pay.amount)            AS total_revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p  ON p.product_id = o.product_id
JOIN payments pay ON pay.order_id = o.order_id
WHERE pay.status = 'COMPLETED'
GROUP BY c.city, p.category
ORDER BY total_revenue DESC;
"""
```

---

## 6. Sample Input
- **Customers Historical (`customers_historical.csv`):**
  ```csv
  customer_id,name,email,city
  1,  asha rao ,Asha@Mail.com,mumbai
  2,RAVI KUMAR,ravi@mail.com,Delhi
  2,RAVI KUMAR,ravi@mail.com,Delhi
  5,tom paul,tom_at_mail.com,Chennai
  ```
  *(Record 5 has an invalid email format without `@`, triggering quarantine).*

---

## 7. Sample Output
```text
======================================================================
PIPELINE RUN: HISTORICAL DATA (first load)
======================================================================
Loaded into 'customers': 3 valid rows (1 duplicate dropped, 1 rejected for invalid email)
Loaded into 'products' : 4 valid rows
Loaded into 'orders'   : 4 valid rows
Loaded into 'payments' : 4 valid rows

======================================================================
PIPELINE RUN: NEWLY ARRIVING DATA (incremental load)
======================================================================
Customers before: 3 | Delta added: 2 | Customers now: 5
Orders before   : 4 | Delta added: 2 | Orders now   : 6

======================================================================
REPORT: E-Commerce Executive Revenue Report
======================================================================
1. Revenue by city and category (completed orders):
   city    category  orders  revenue
 Mumbai Electronics       2  75000.0
  Delhi    Clothing       2   3500.0
   Pune Electronics       1  30000.0

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully engineered a complete, production-grade e-commerce data pipeline integrating multi-table ingestion, automated data validation and quarantine isolation, Change Data Capture incremental loading into SQLite, and multi-dimensional analytical reporting.

---

## 9. Learning Outcome
- Mastered end-to-end data engineering architecture across multi-table relational ecosystems.
- Implemented production-grade validation gates and rejection routing mechanisms.
- Acquired deep understanding of incremental loading and Change Data Capture (CDC) design patterns.
- Formulated complex multi-table analytical SQL queries for business intelligence reporting.
