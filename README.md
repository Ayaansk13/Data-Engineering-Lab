# Data Engineering Laboratory Coursework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5%2B-E25A1C.svg?logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x%2F3.x-017CEE.svg?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0%2B-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Coursework-Completed-brightgreen.svg)]()

> A comprehensive, hands-on laboratory repository containing end-to-end practical implementations for the **Data Engineering** course. This repository spans semi-structured data parsing, relational and NoSQL database modeling, exploratory data analysis and noise elimination, REST API ingestion, workflow orchestration using Apache Airflow, distributed big data processing with Apache PySpark, and enterprise-grade incremental ETL pipelines.

---

## Author Information

- **Student Name:** Mohammad Ayaan Sajid Shaikh
- **Roll Number:** 47
- **Student ID:** 5135870
- **Course:** Data Engineering Laboratory

---

## Course Objectives

The objective of this laboratory coursework is to develop industry-relevant competency in:
1. **Data Ingestion & Parsing:** Ingesting, parsing, and validating diverse data formats (CSV, JSON, XML, HTML, plain text, and fixed-width binary structures).
2. **Database Engineering:** Designing normalized relational database schemas (SQLite) and schema-flexible document stores (MongoDB), enforcing constraints, and executing complex CRUD operations.
3. **Data Quality & Preprocessing:** Detecting and eliminating statistical noise (IQR method), applying variance thresholding for feature selection, and performing Exploratory Data Analysis (EDA).
4. **API Integration & Web Ingestion:** Consuming RESTful web APIs, normalizing nested JSON payloads, and blending online data with offline flat-file sources.
5. **Workflow Orchestration:** Automating, scheduling, and monitoring multi-stage ETL tasks using Apache Airflow Directed Acyclic Graphs (DAGs).
6. **Distributed Data Processing:** Leveraging Apache PySpark DataFrames and Spark SQL to perform distributed transformations, aggregations, deduplication, and joins on large datasets.
7. **Production ETL Architecture:** Implementing robust, idempotent batch and incremental ETL pipelines featuring anomaly isolation (Dead-Letter / Quarantine Pattern), schema validation, and Change Data Capture (CDC).

---

## Repository Structure

```text
Data-Engineering-Lab/
├── Practical-01/          # Data Parsing, Binary Files, Regex, and SQL CRUD
│   ├── Data_Parsing.ipynb
│   ├── Binary_File_Operations.ipynb
│   ├── Regex_Operations.ipynb
│   ├── SQL_CRUD.ipynb
│   └── README.md
├── Practical-02/          # Relational Database Design & SQL Operations
│   ├── Relational_Database_Design_and_CRUD.ipynb
│   └── README.md
├── Practical-03/          # NoSQL Database Operations using MongoDB
│   ├── MongoDB_NoSQL_Operations.ipynb
│   ├── practical_03_mongodb.js
│   └── README.md
├── Practical-04/          # Noise Elimination, Feature Selection & EDA
│   ├── EDA_and_Feature_Selection.ipynb
│   └── README.md
├── Practical-05/          # REST API & Flat-File Data Integration
│   ├── API_and_Flat_File_Data_Extraction.ipynb
│   ├── locations.csv
│   └── README.md
├── Practical-06/          # Workflow Orchestration with Apache Airflow
│   ├── Airflow_Data_Pipeline_DAG.ipynb
│   ├── data_extraction.py
│   ├── data_pipeline_dag.py
│   └── README.md
├── Practical-07/          # Batch ETL Pipeline with Quality Validation
│   ├── Batch_ETL_Pipeline_and_Validation.ipynb
│   └── README.md
├── Practical-08/          # Distributed Big Data Processing with PySpark
│   ├── PySpark_DataFrame_Operations.ipynb
│   └── README.md
├── Practical-09/          # Incremental E-Commerce ETL Pipeline (CDC)
│   ├── Incremental_ETL_Data_Pipeline.ipynb
│   └── README.md
├── .gitattributes
├── requirements.txt
└── README.md
```

---

## Practical Index

| Practical | Experiment Title | Key Tools & Libraries | Experiment Notebooks |
| :--- | :--- | :--- | :--- |
| **[Practical-01](./Practical-01/)** | Semi-Structured Data Parsing, Binary Structs, Regex, and SQL CRUD | `csv`, `json`, `xml.etree`, `html.parser`, `struct`, `re`, `sqlite3` | [`Data_Parsing.ipynb`](./Practical-01/Data_Parsing.ipynb)<br>[`Binary_File_Operations.ipynb`](./Practical-01/Binary_File_Operations.ipynb)<br>[`Regex_Operations.ipynb`](./Practical-01/Regex_Operations.ipynb)<br>[`SQL_CRUD.ipynb`](./Practical-01/SQL_CRUD.ipynb) |
| **[Practical-02](./Practical-02/)** | Relational Database Schema Design & Multi-Table SQL CRUD | `sqlite3`, SQL DDL/DML | [`Relational_Database_Design_and_CRUD.ipynb`](./Practical-02/Relational_Database_Design_and_CRUD.ipynb) |
| **[Practical-03](./Practical-03/)** | NoSQL Document Database Operations using MongoDB | `MongoDB 7.0`, `mongosh`, BSON | [`MongoDB_NoSQL_Operations.ipynb`](./Practical-03/MongoDB_NoSQL_Operations.ipynb) |
| **[Practical-04](./Practical-04/)** | Noise Elimination, Feature Selection, and Exploratory Data Analysis | `pandas`, `numpy`, `scikit-learn`, `matplotlib` | [`EDA_and_Feature_Selection.ipynb`](./Practical-04/EDA_and_Feature_Selection.ipynb) |
| **[Practical-05](./Practical-05/)** | Ingesting & Harmonizing REST API and Flat-File Datasets | `requests`, `pandas`, REST API | [`API_and_Flat_File_Data_Extraction.ipynb`](./Practical-05/API_and_Flat_File_Data_Extraction.ipynb) |
| **[Practical-06](./Practical-06/)** | Pipeline Orchestration & Scheduling with Apache Airflow | `apache-airflow`, `BashOperator`, `EmptyOperator` | [`Airflow_Data_Pipeline_DAG.ipynb`](./Practical-06/Airflow_Data_Pipeline_DAG.ipynb) |
| **[Practical-07](./Practical-07/)** | Multi-Source Batch ETL Pipeline with Anomaly Quarantine & Validation | `pandas`, `sqlite3`, Data Quality Auditing | [`Batch_ETL_Pipeline_and_Validation.ipynb`](./Practical-07/Batch_ETL_Pipeline_and_Validation.ipynb) |
| **[Practical-08](./Practical-08/)** | Distributed Big Data Transformations with Apache PySpark | `pyspark`, Spark SQL, SparkSession | [`PySpark_DataFrame_Operations.ipynb`](./Practical-08/PySpark_DataFrame_Operations.ipynb) |
| **[Practical-09](./Practical-09/)** | End-to-End E-Commerce Data Pipeline with Incremental CDC | `pandas`, `sqlite3`, CDC Architecture | [`Incremental_ETL_Data_Pipeline.ipynb`](./Practical-09/Incremental_ETL_Data_Pipeline.ipynb) |

---

## Technologies & Frameworks Used

- **Programming Language:** Python 3.8+
- **Data Manipulation & Analysis:** Pandas, NumPy
- **Machine Learning & Preprocessing:** Scikit-learn (`VarianceThreshold`)
- **Data Visualization:** Matplotlib
- **Database Engines:** SQLite 3 (RDBMS), MongoDB 7.0+ (NoSQL Document Store)
- **Workflow Orchestrator:** Apache Airflow 2.x / 3.x
- **Distributed Computing:** Apache Spark 3.5+ via PySpark
- **Networking & Serialization:** Requests, Struct, Regular Expressions (`re`), ElementTree XML

---

## Software Requirements

Ensure your development environment meets the following specifications:
- **Operating System:** Linux (Ubuntu 20.04+ recommended), macOS, or Windows (via WSL2 recommended for Airflow/MongoDB).
- **Python:** Version 3.8 or higher.
- **Java Runtime:** Java Development Kit (JDK 8 or 11) installed and configured in `JAVA_HOME` (required for PySpark).
- **MongoDB:** Community Edition 7.0+ along with `mongosh`.
- **Apache Airflow:** Version 2.8+ or 3.x.

---

## Installation & Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Ayaansk13/Data-Engineering-Lab.git
cd Data-Engineering-Lab
```

### 2. Create and Activate a Virtual Environment
```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup MongoDB (Required for Practical-03)
On Debian/Ubuntu or Google Colab:
```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --yes --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org mongodb-mongosh
sudo systemctl start mongod
```

### 5. Launch Jupyter Lab / Notebook
```bash
jupyter lab
```
Navigate to any `Practical-XX` folder to explore, inspect, and execute the experiments.

---

## Summary of Results

All nine practical experiments have been verified, documented, and tested. The experiments cover the full lifecycle of data engineering—from raw file extraction and schema modeling to workflow orchestration and fault-tolerant incremental loading.

---
*Maintained by Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870).*
