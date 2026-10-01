import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("sample.xml")
root = tree.getroot()

data = []

for student in root.findall("student"):
    data.append({
        "ID": student.find("ID").text,
        "Name": student.find("Name").text,
        "Age": student.find("Age").text,
        "Course": student.find("Course").text,
        "Marks": student.find("Marks").text
    })

df = pd.DataFrame(data)

print(df)

print("\nMissing Values")
print(df.isnull().sum())
