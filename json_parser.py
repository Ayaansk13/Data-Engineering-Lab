import pandas as pd

df = pd.read_json("sample.json")

print(df)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())
