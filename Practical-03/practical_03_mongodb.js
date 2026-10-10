// Practical 03: MongoDB NoSQL Operations Script
// Author: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)

print("\n## Step 1: Insert Single Document");
print('Query: db.items.insertOne({ name: "laptop", price: 999 });');
var insertOneRes = db.items.insertOne({ name: "laptop", price: 999 });
printjson(insertOneRes);

print("\n## Step 2: View Inserted Document");
print("Query: db.items.find();");
printjson(db.items.find().toArray());

print("\n## Step 3: Insert Multiple Documents");
print("Query: db.products.insertMany([...3 products...]);");
var insertManyRes = db.products.insertMany([
  { name: "phone", price: 500, stock: 10 },
  { name: "tablet", price: 300, stock: 5 },
  { name: "watch", price: 150, stock: 0 }
]);
printjson(insertManyRes);

print("\n## Step 4: View Products in Formatted JSON");
print("Query: db.products.find().pretty();");
printjson(db.products.find().toArray());

print("\n" + "=".repeat(40));
print("Submitted by: Mohammad Ayaan Sajid Shaikh");
print("=".repeat(40));
