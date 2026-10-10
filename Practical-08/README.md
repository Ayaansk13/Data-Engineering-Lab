# Practical-08: Distributed Big Data Processing using Apache PySpark DataFrames

---

## 1. Aim
To execute distributed data processing operations using Apache PySpark, including SparkSession initialization, schema inference, DataFrame transformations, conditional filtering, categorical grouping, aggregate metrics computation, duplicate record elimination, and relational dataset joins using both PySpark DataFrame DSL and Spark SQL.

---

## 2. Theory

### 2.1 The Apache Spark Distributed Computing Framework
Traditional data analysis tools like Pandas are bound to single-node memory limits. Apache Spark provides distributed computing capabilities across clusters:
- **SparkSession:** The unified entry point for reading data, managing cluster resources, and executing SQL queries.
- **Catalyst Optimizer:** Generates optimized logical and physical query execution plans (predicate pushdown, projection pruning).
- **Tungsten Engine:** Provides low-level off-heap memory management and whole-stage code generation for near-hardware execution speeds.
- **Lazy Evaluation:** Transformations (`filter`, `groupBy`, `join`) build a Directed Acyclic Graph (DAG) of computations and are only materialized when an Action (`show`, `count`, `collect`) is invoked.

### 2.2 PySpark DataFrame Operations
- **Schema Inference:** Spark inspects file headers and sample records to automatically infer data types (`IntegerType`, `StringType`, `DoubleType`).
- **Narrow vs. Wide Transformations:**
  - *Narrow:* `filter()` and `select()` operate independently within individual partitions without network shuffling.
  - *Wide:* `groupBy()` and `join()` require data shuffling across cluster nodes to group records sharing identical partition keys.
- **Spark SQL Integration:** DataFrames can be registered as temporary views (`createOrReplaceTempView`), enabling standard ANSI SQL querying over distributed data.

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Big Data Engine:** Apache Spark 3.4+ (`pyspark`)
- **Runtime Dependency:** Java Development Kit (JDK 8 or 11)
- **Environment:** Jupyter Notebook / Google Colab / Linux

---

## 4. Procedure
1. Initialize a local `SparkSession` with master set to `local[*]`.
2. Generate synthetic CSV datasets:
   - `sales.csv`: `order_id`, `product`, `category`, `sales`, `quantity` (with injected duplicate rows).
   - `discounts.csv`: `category`, `discount_pct`.
3. **Task 1: Read & Schema Inspection:** Load `sales.csv` using `spark.read.csv(..., header=True, inferSchema=True)` and display the schema using `.printSchema()`.
4. **Task 2: Filtering & Grouping:** Filter sales records where `sales > 1000`; group by `category` and calculate total revenue and total units sold.
5. **Task 3: Deduplication:** Identify and drop duplicate records across composite keys using `df.dropDuplicates()`.
6. **Task 4: Distributed Join:** Perform an inner join between the deduplicated sales DataFrame and the discounts dataset on the `category` attribute.
7. **Task 5: Aggregate Metrics & Spark SQL:** Calculate average sales by product category using the DataFrame DSL; register a temporary view `sales` and compute identical metrics via Spark SQL.

---

## 5. Code Explanation

### SparkSession & Schema Loading
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("PySpark_Data_Engineering_Lab") \
    .master("local[*]") \
    .getOrCreate()

# Ingest CSV with automated schema inference
sales_df = spark.read.csv("sales.csv", header=True, inferSchema=True)
sales_df.printSchema()
```

### Deduplication, Joining & Aggregations
```python
# Task 3: Drop duplicates
dedup_df = sales_df.dropDuplicates(["order_id", "product"])

# Task 4: Relational Inner Join with Discounts
discounts_df = spark.read.csv("discounts.csv", header=True, inferSchema=True)
joined_df = dedup_df.join(discounts_df, on="category", how="inner")
joined_df.show()

# Task 5: Aggregations using DataFrame API & Spark SQL
avg_df = (dedup_df.groupBy("category")
          .agg(F.round(F.avg("sales"), 2).alias("avg_sales"))
          .orderBy(F.desc("avg_sales")))
avg_df.show()

# Equivalent Spark SQL
dedup_df.createOrReplaceTempView("sales")
spark.sql("""
    SELECT category, ROUND(AVG(sales), 2) AS avg_sales
    FROM sales
    GROUP BY category
    ORDER BY avg_sales DESC
""").show()
```

---

## 6. Sample Input
- **Sample Sales Data (`sales.csv`):**
  ```csv
  order_id,product,category,sales,quantity
  1,Laptop,Electronics,55000,2
  2,Phone,Electronics,20000,5
  2,Phone,Electronics,20000,5
  3,Tablet,Electronics,30000,3
  4,Shirt,Clothing,800,10
  5,Jeans,Clothing,1500,4
  5,Jeans,Clothing,1500,4
  ```
- **Discounts Data (`discounts.csv`):**
  ```csv
  category,discount_pct
  Electronics,10
  Clothing,20
  ```

---

## 7. Sample Output
```text
root
 |-- order_id: integer (nullable = true)
 |-- product: string (nullable = true)
 |-- category: string (nullable = true)
 |-- sales: integer (nullable = true)
 |-- quantity: integer (nullable = true)

TASK 2: Filtering (sales > 1000)
+--------+-------+-----------+-----+--------+
|order_id|product|   category|sales|quantity|
+--------+-------+-----------+-----+--------+
|       1| Laptop|Electronics|55000|       2|
|       2|  Phone|Electronics|20000|       5|
|       3| Tablet|Electronics|30000|       3|
|       5|  Jeans|   Clothing| 1500|       4|
+--------+-------+-----------+-----+--------+

TASK 3: Deduplication
Raw record count: 7
Deduplicated record count: 5

TASK 5: Average Sales by Category
+-----------+---------+
|   category|avg_sales|
+-----------+---------+
|Electronics|  35000.0|
|   Clothing|   1150.0|
+-----------+---------+

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully deployed a local PySpark runtime, inferred dataset schemas, executed distributed narrow and wide transformations, eliminated duplicate records, and executed relational joins using both PySpark DataFrame DSL and Spark SQL.

---

## 9. Learning Outcome
- Understood Apache Spark's distributed execution model, SparkSession management, and lazy evaluation.
- Mastered PySpark DataFrame operations including `select`, `filter`, `groupBy`, and `agg`.
- Gained practical skills in distributed data deduplication and partitioned dataset joins.
- Demonstrated interoperability between procedural PySpark DataFrame APIs and declarative Spark SQL.
