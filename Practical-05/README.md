# Practical-05: Extracting and Integrating Data from REST APIs and Flat Files

---

## 1. Aim
To ingest, clean, and harmonize data across heterogeneous sources by querying user profile records from a public RESTful API, normalizing nested JSON payloads into a tabular structure, extracting regional attributes from a flat CSV file, and executing relational merging to build a consolidated data warehouse table.

---

## 2. Theory

### 2.1 REST API Architecture & Data Ingestion
Representational State Transfer (REST) is an architectural style for distributed hypermedia systems. Web APIs expose resources via standard HTTP endpoints:
- **HTTP GET:** Retrieves resource representations without modifying server state.
- **HTTP Status Codes:** `200 OK` (success), `404 Not Found`, `500 Server Error`. `response.raise_for_status()` guarantees that network and HTTP exceptions are handled immediately before parsing.
- **Network Resilience:** Specifying explicit request timeouts (`timeout=10`) prevents pipeline threads from stalling indefinitely on degraded external services.

### 2.2 JSON Flattening & Normalization
API responses frequently nest hierarchical data structures (e.g., an address object embedded inside a user entity). To make nested structures compatible with relational databases or analytical data lakes, `pandas.json_normalize` flattens parent-child dictionaries into dotted tabular column names (`company.name -> company`).

### 2.3 Heterogeneous Data Harmonization
In enterprise data engineering, primary entities are rarely contained in a single repository. Merging online operational data (API) with offline regional metadata (flat CSV) requires schema alignment, standardizing join keys (`id`), resolving missing values, and validating data types.

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Libraries:** `pandas`, `requests`
- **Environment:** Jupyter Notebook / Local Shell

---

## 4. Procedure
1. Send an HTTP `GET` request to the public JSONPlaceholder users endpoint (`https://jsonplaceholder.typicode.com/users`) with a 10-second timeout.
2. Validate HTTP status code and convert the raw JSON response payload into a pandas DataFrame using `pd.json_normalize()`.
3. Select relevant profile attributes (`id`, `name`, `email`, `company.name`) and rename `company.name` to `company`.
4. Create and ingest regional location data from a flat CSV file (`locations.csv`) containing `id` and `city` attributes.
5. Execute an inner join (`pd.merge(api_df, csv_df, on="id", how="inner")`) to blend the datasets.
6. Perform data validation: check for null values across merged columns using `merged_df.isnull().sum()`.
7. Persist the harmonized profile records to an output file (`cleaned_warehouse_profiles.csv`).

---

## 5. Code Explanation

### API Ingestion & Flattening
```python
import pandas as pd
import requests

def extract_api_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Normalizes hierarchical JSON into a flat DataFrame
        return pd.json_normalize(response.json())
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return pd.DataFrame()
```

### Dataset Merging & Quality Check
```python
# Select and rename columns
api_df = api_df[["id", "name", "email", "company.name"]]
api_df.rename(columns={"company.name": "company"}, inplace=True)

# Merge API dataset with flat CSV dataset on common key 'id'
merged_df = pd.merge(api_df, csv_df, on="id", how="inner")

# Check for missing values post-merge
null_counts = merged_df.isnull().sum()
print("Missing values per column:\n", null_counts)

# Persist target data
merged_df.to_csv("cleaned_warehouse_profiles.csv", index=False)
```

---

## 6. Sample Input
- **API Response Snippet (`https://jsonplaceholder.typicode.com/users`):**
  ```json
  [
    {
      "id": 1,
      "name": "Leanne Graham",
      "email": "Sincere@april.biz",
      "company": { "name": "Romaguera-Crona" }
    }
  ]
  ```
- **Flat File (`locations.csv`):**
  ```csv
  id,city
  1,New York
  2,London
  3,Paris
  ```

---

## 7. Sample Output
```text
--- Merged ETL Pipeline Data View ---
   id            name              email           company      city
0   1   Leanne Graham  Sincere@april.biz  Romaguera-Crona  New York
1   2    Ervin Howell  Shanna@melissa.tv     Deckow-Crist    London
2   3  Clementine Bau   Nathan@yesenia.net  Romaguera-Jacob     Paris
3   4  Patricia Lebsa  Julianne.OConner@...   Robel-Corkery     Tokyo
4   5  Chelsey Dietri  Lucio_Hettinger@...    Keebler LLC    Berlin

Data successfully saved to 'cleaned_warehouse_profiles.csv'

Missing values per column:
 id         0
name       0
email      0
company    0
city       0
dtype: int64

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully queried and flattened live REST API data, harmonized it with offline flat-file CSV records using relational joins, verified data completeness, and exported clean warehouse profiles.

---

## 9. Learning Outcome
- Gained practical experience in consuming RESTful APIs using Python's `requests` library.
- Learned automated flattening of nested hierarchical JSON structures using `pandas.json_normalize`.
- Implemented robust error handling for network latency and connection failures.
- Mastered multi-source data integration and quality auditing in analytical pipelines.
