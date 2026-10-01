import pandas as pd

df = pd.read_csv("sample.csv")

print(df)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nStatistics")
print(df.describe())
