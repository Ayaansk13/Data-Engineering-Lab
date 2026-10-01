import pandas as pd

tables = pd.read_html("sample.html")

df = tables[0]

print(df)

print("\nMissing Values")
print(df.isnull().sum())
