# Practical-07: Batch ETL Pipeline with Data Quality Validation and Incremental Loading

---

## 1. Aim
To develop a modular batch ETL (Extract, Transform, Load) pipeline using Python and SQLite that extracts multi-format source data (CSV and JSON), performs data normalization, applies rigorous data validation checks, isolates anomalous records into a dead-letter quarantine, and executes idempotent incremental database loading.

---

## 2. Theory

### 2.1 The Modern Batch ETL Architecture
In batch data architectures, data arrives periodically in scheduled chunks. The lifecycle consists of four robust stages:
1. **Extract:** Ingesting multi-source records (e.g., historical CSVs, streaming JSON logs).
2. **Transform & Clean:**
   - Standardizing string casing (e.g., trimming whitespace and converting to title case).
   - Type casting and ISO date normalization (`YYYY-MM-DD`).
3. **Data Quality Validation (Quarantine Pattern):**
   - Applying rule-based validation filters prior to database insertion.
   - Valid records proceed to the load phase.
   - Invalid records (missing names, non-positive amounts, invalid dates) are redirected to an anomaly quarantine with explicit failure reasons.
4. **Load (Idempotent & Incremental):**
   - Deduplicating incoming records against existing warehouse primary keys to ensure pipeline reruns do not create duplicates.

### 2.2 Data Quality & Business Rules Enforced
- **Rule 1 (Completeness):** `customer_name` must be non-null and non-empty.
- **Rule 2 (Numerical Sanity):** `amount` must be greater than zero ($> 0$).
- **Rule 3 (Temporal Validity):** `order_date` must match valid format `%Y-%m-%d` and cannot occur in the future ($t \le t_{\text{today}}$).

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Libraries:** `pandas`, `sqlite3`, `json`, `os`
- **Environment:** Jupyter Notebook / Local Shell

---

## 4. Procedure
1. **Source Generation:** Generate mock batch files:
   - `orders_jan.csv`: Messy historical records (extra whitespace, duplicates, negative amounts).
   - `orders_feb.csv`: Second batch with valid and invalid entries.
   - `orders_mar.csv`: Incremental batch for delta testing.
   - `orders.json`: JSON format orders to test multi-format ingestion.
2. **Task 1: Single CSV Processing:** Extract, clean whitespace, validate, and load into SQLite table `orders`.
3. **Task 2: Multi-File Ingestion:** Ingest multiple monthly CSV files (`jan`, `feb`), concatenate via `pd.concat`, and deduplicate.
4. **Task 3: Semi-Structured JSON Processing:** Ingest JSON orders, extract required fields, harmonize schemas, and persist to database.
5. **Task 4: Anomaly Isolation:** Apply Boolean masks to identify failed records; isolate them into a separate rejected dataset alongside explanatory tags (`"missing customer_name"`, `"non-positive amount"`).
6. **Task 5: Pre-Load Validation:** Run defensive schema assertions (checking for required column presence and non-null constraints) before opening database transactions.
7. **Task 6: Incremental Loading:** Extract only records whose `order_id` does not currently exist in the SQLite database (`WHERE order_id NOT IN (...)`) and append the delta rows.

---

## 5. Code Explanation

### Anomaly Isolation Engine
```python
def find_reasons(df):
    """Evaluates data quality rules and tags rejection reasons."""
    reasons = pd.Series("", index=df.index, dtype=object)
    
    # Check 1: Empty or missing customer names
    name = df["customer_name"].astype("string").str.strip()
    mask1 = name.isna() | (name == "")
    reasons[mask1] = reasons[mask1].apply(lambda s: (s + "; " if s else "") + "missing customer_name")
    
    # Check 2: Non-positive monetary amounts
    amount = pd.to_numeric(df["amount"], errors="coerce")
    mask2 = amount.isna() | (amount <= 0)
    reasons[mask2] = reasons[mask2].apply(lambda s: (s + "; " if s else "") + "non-positive amount")
    
    return reasons

def clean_invalid(df):
    reasons = find_reasons(df)
    valid_df = df[reasons == ""].copy()
    rejected_df = df[reasons != ""].copy()
    rejected_df["rejection_reason"] = reasons[reasons != ""]
    return valid_df, rejected_df
```

### Incremental Loading Logic
```python
def incremental_load(df, table="orders", key="order_id"):
    conn = sqlite3.connect("warehouse.db")
    existing_keys = set(pd.read_sql(f"SELECT {key} FROM {table}", conn)[key])
    # Filter only newly arriving records not already in database
    new_records = df[~df[key].isin(existing_keys)]
    if not new_records.empty:
        new_records.to_sql(table, conn, if_exists="append", index=False)
    conn.close()
```

---

## 6. Sample Input
- **Raw CSV Data (`orders_jan.csv`):**
  ```csv
  order_id,customer_name,amount,order_date
  1,  asha rao ,100,2026-01-05
  2,RAVI KUMAR,200,2026-01-12
  2,RAVI KUMAR,200,2026-01-12
  3,,150,2026-01-15
  4,Meena,-50,2026-01-20
  ```

---

## 7. Sample Output
```text
======================================================================
TASK 1: Single CSV -> clean -> transform -> database
======================================================================
Rows extracted: 5 | Valid rows: 3 | Rejected rows: 2
Loaded 3 clean records into SQLite table 'orders'.

======================================================================
TASK 4: Identify and remove invalid records
======================================================================
Rejected records quarantine:
   order_id customer_name  amount  order_date                 rejection_reason
3         3           NaN   150.0  2026-01-15            missing customer_name
4         4         Meena   -50.0  2026-01-20              non-positive amount

======================================================================
TASK 6: Incremental loading
======================================================================
Database row count before incremental load: 3
Incoming batch: 3 records (1 duplicate, 2 new)
Inserted 2 delta records. Total warehouse rows now: 5

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully built a multi-stage batch ETL pipeline capable of ingesting diverse file types, auditing data against business validation rules, quarantining anomalies with explicit failure reasons, and performing idempotent incremental database loads.

---

## 9. Learning Outcome
- Mastered multi-source data extraction (CSV, JSON) and relational loading using Pandas and SQLite.
- Implemented enterprise-grade anomaly routing (Dead-Letter Pattern) to protect analytical databases from bad data.
- Built defensive validation gates enforcing completeness and type integrity.
- Designed duplicate-safe incremental load mechanisms using primary key delta filtering.
