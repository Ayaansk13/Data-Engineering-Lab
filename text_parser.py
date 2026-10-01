import pandas as pd

df = pd.read_csv("sample.txt")

print("Student Data")
print(df)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nData Types")
print(df.dtypes)
