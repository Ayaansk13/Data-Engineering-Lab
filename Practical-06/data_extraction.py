# Practical 06 Helper: Data Extraction Script
# Author: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)
import pandas as pd
import requests

STUDENT_NAME = "Mohammad Ayaan Sajid Shaikh"

def extract_api_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return pd.json_normalize(data)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return pd.DataFrame()

def extract_csv_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    api_url = "https://jsonplaceholder.typicode.com/users"
    api_df = extract_api_data(api_url)
    if not api_df.empty:
        api_df = api_df[["id", "name", "email", "company.name"]]
        api_df.rename(columns={"company.name": "company"}, inplace=True)

    csv_file = "locations.csv"
    pd.DataFrame({
        "id": list(range(1, 11)),
        "city": ["New York", "London", "Paris", "Tokyo", "Berlin",
                 "Delhi", "Sydney", "Moscow", "Cairo", "Beijing"]
    }).to_csv(csv_file, index=False)

    csv_df = extract_csv_data(csv_file)
    if not api_df.empty and not csv_df.empty:
        merged_df = pd.merge(api_df, csv_df, on="id", how="inner")
        print("\n--- Merged ETL Pipeline Data View ---")
        print(merged_df.head())
        merged_df.to_csv("cleaned_warehouse_profiles.csv", index=False)
        print("\nData successfully saved to 'cleaned_warehouse_profiles.csv'")
        print("\nMissing values per column:\n", merged_df.isnull().sum())

    print("\n" + "=" * 40)
    print("Submitted by:", STUDENT_NAME)
    print("=" * 40)
