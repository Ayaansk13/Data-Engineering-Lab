# Practical-03: NoSQL Database Operations using MongoDB

---

## 1. Aim
To install, configure, and operate a document-oriented NoSQL database management system using MongoDB and the MongoDB Shell (`mongosh`), design a flexible BSON document schema, and execute fundamental NoSQL CRUD operations including single/batch insertions, querying, and formatted JSON projections.

---

## 2. Theory

### 2.1 Relational vs. Document-Oriented NoSQL
Unlike relational databases that enforce rigid tabular schemas with foreign key joins, MongoDB is a document-oriented NoSQL database designed for horizontal scalability, unstructured/semi-structured data agility, and high-throughput workloads:
- **Documents:** Data is persisted in BSON (Binary JSON) format consisting of field-and-value pairs.
- **Collections:** Groups of documents equivalent to relational tables, but schema-flexible (documents within the same collection can have differing fields).
- **Primary Key (`_id`):** Every MongoDB document automatically receives a unique 12-byte `ObjectId` consisting of a 4-byte timestamp, 5-byte random value, and 3-byte incrementing counter.

### 2.2 CRUD Operations in MongoDB
- **Create:** `db.collection.insertOne()` and `db.collection.insertMany()` persist documents atomically at the document level.
- **Read:** `db.collection.find()` retrieves documents matching a query filter; `.pretty()` formats JSON output with indentation.
- **Update:** `db.collection.updateOne()`, `updateMany()`, or replacement operators (`$set`, `$inc`).
- **Delete:** `db.collection.deleteOne()` and `deleteMany()`.

---

## 3. Software Requirements
- **Database Server:** MongoDB Community Server 7.0+
- **Interactive Shell:** MongoDB Shell (`mongosh`)
- **Environment:** Ubuntu Linux / Google Colab / WSL
- **Language:** JavaScript (Mongo Shell Scripting) / Python

---

## 4. Procedure
1. Import the official MongoDB public GPG signing key and configure the APT package source repository.
2. Install MongoDB packages: `mongodb-org` and `mongodb-mongosh`.
3. Initialize the `mongod` background database daemon with dedicated log and data paths (`/var/lib/mongodb`).
4. Connect to the database instance (`use practical3`) via `mongosh`.
5. Execute script `practical_03_mongodb.js`:
   - Step 1: Insert a single item document into collection `items`.
   - Step 2: Query the `items` collection to verify document insertion and inspect the auto-generated `_id`.
   - Step 3: Insert multiple product documents into collection `products` with varied attributes (`name`, `price`, `stock`).
   - Step 4: Query all documents from `products` and output them as formatted JSON.

---

## 5. Code Explanation

### MongoDB Operations Script (`practical_03_mongodb.js`)
```javascript
// Step 1: Insert a single document into 'items' collection
var insertOneRes = db.items.insertOne({ 
    name: "laptop", 
    price: 999 
});
printjson(insertOneRes);

// Step 2: Query the inserted document
var items = db.items.find().toArray();
printjson(items);

// Step 3: Insert multiple documents with heterogeneous schema
var insertManyRes = db.products.insertMany([
    { name: "phone", price: 500, stock: 10 },
    { name: "tablet", price: 300, stock: 5 },
    { name: "watch", price: 150, stock: 0 }
]);
printjson(insertManyRes);

// Step 4: Formatted retrieval of all product documents
printjson(db.products.find().toArray());
```

---

## 6. Sample Input
- **Single Document (items):**
  ```json
  { "name": "laptop", "price": 999 }
  ```
- **Multiple Documents (products):**
  ```json
  [
    { "name": "phone", "price": 500, "stock": 10 },
    { "name": "tablet", "price": 300, "stock": 5 },
    { "name": "watch", "price": 150, "stock": 0 }
  ]
  ```

---

## 7. Sample Output
```text
switched to db practical3

## Step 1: Insert Single Document
Query: db.items.insertOne({ name: "laptop", price: 999 });
{
  acknowledged: true,
  insertedId: ObjectId('6ac904bbaa1299817862fab1')
}

## Step 2: View Inserted Document
Query: db.items.find();
[
  {
    _id: ObjectId('6ac904bbaa1299817862fab1'),
    name: 'laptop',
    price: 999
  }
]

## Step 3: Insert Multiple Documents
Query: db.products.insertMany([...3 products...]);
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('6ac904bbaa1299817862fab2'),
    '1': ObjectId('6ac904bbaa1299817862fab3'),
    '2': ObjectId('6ac904bbaa1299817862fab4')
  }
}

## Step 4: View Products in Formatted JSON
Query: db.products.find().pretty();
[
  {
    _id: ObjectId('6ac904bbaa1299817862fab2'),
    name: 'phone',
    price: 500,
    stock: 10
  },
  {
    _id: ObjectId('6ac904bbaa1299817862fab3'),
    name: 'tablet',
    price: 300,
    stock: 5
  },
  {
    _id: ObjectId('6ac904bbaa1299817862fab4'),
    name: 'watch',
    price: 150,
    stock: 0
  }
]

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully deployed MongoDB Community Server 7.0, initialized the database daemon, connected via `mongosh`, and performed document-level CRUD operations on schema-flexible BSON collections.

---

## 9. Learning Outcome
- Understood the design differences between relational schemas and NoSQL document collections.
- Learned the anatomy of BSON documents and auto-generated `ObjectId` tokens.
- Mastered document creation, retrieval, and formatting operations using `mongosh`.
- Developed practical skills for selecting NoSQL stores when dealing with rapidly evolving semi-structured payloads.
