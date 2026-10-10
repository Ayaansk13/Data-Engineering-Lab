# Practical-02: Relational Database Schema Design and SQL Operations

---

## 1. Aim
To design, implement, and validate a normalized relational database schema using SQLite, enforce primary and foreign key constraints, populate data via batch execution, and perform comprehensive SQL CRUD operations including multi-table inner joins, conditional updates, and transactional deletes.

---

## 2. Theory

### 2.1 Relational Data Modeling & Normalization
A relational database organizes data into formal mathematical relations (tables) with strict schemas:
- **Primary Key (PK):** A column (or set of columns) that uniquely identifies each entity record.
- **Foreign Key (FK):** A referential constraint linking a column in a child table to the primary key of a parent table, guaranteeing referential integrity.
- **Normalization (1NF, 2NF, 3NF):** Structuring schemas to eliminate redundancy, avoid update/delete anomalies, and ensure data dependencies are logical.

### 2.2 Relational Algebra & Multi-Table Joins
Inner joins ($owtie$) merge records from two or more tables based on matching predicate conditions:
$$\text{Enrollments} \bowtie_{\text{student\_id}} \text{Students} \bowtie_{\text{course\_id}} \text{Courses}$$
This allows reconstructing denormalized reporting views without persisting redundant text across multiple tables.

### 2.3 SQLite Engine Architecture
SQLite is an in-process, serverless, self-contained relational database management engine. By default in SQLite, foreign key enforcement must be activated explicitly per session using:
```sql
PRAGMA foreign_keys = ON;
```

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Database Engine:** SQLite 3 (built-in `sqlite3`)
- **Environment:** Jupyter Notebook / Local Shell

---

## 4. Procedure
1. Establish a persistent SQLite database connection (`college.db`) and create a database cursor.
2. Execute a DDL script defining tables:
   - `Students`: `student_id` (PK AUTOINCREMENT), `name` (TEXT NOT NULL), `email` (TEXT UNIQUE), `age` (INTEGER).
   - `Courses`: `course_id` (PK AUTOINCREMENT), `title` (TEXT NOT NULL), `credits` (INTEGER).
   - `Enrollments`: `enroll_id` (PK AUTOINCREMENT), `student_id` (FK), `course_id` (FK), `grade` (TEXT).
3. Populate tables in batch using `cursor.executemany` with parameterized tuples to prevent SQL injection.
4. Execute an SQL `SELECT` query utilizing `INNER JOIN` across all three tables to generate a student course enrollment report.
5. Perform an SQL `UPDATE` to modify a student's age and verify persistence.
6. Execute a conditional `DELETE` on `Enrollments` where `grade = 'B'` and inspect remaining records.

---

## 5. Code Explanation

### Schema Definition & Constraint Setup
```python
import sqlite3

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Enrollments;

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER
);

CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    credits INTEGER
);

CREATE TABLE Enrollments (
    enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES Students(student_id),
    course_id INTEGER REFERENCES Courses(course_id),
    grade TEXT
);
""")
```

### Relational Join Query
```python
sql_join = """
SELECT s.name, c.title, e.grade
FROM Enrollments e
JOIN Students s ON s.student_id = e.student_id
JOIN Courses c ON c.course_id = e.course_id;
"""
for row in cur.execute(sql_join):
    print(f"Student: {row[0]:<15} | Course: {row[1]:<20} | Grade: {row[2]}")
```

---

## 6. Sample Input
- **Students Data:**
  - `(1, 'Ravi Kumar', 'ravi@example.com', 20)`
  - `(2, 'Asha Sharma', 'asha@example.com', 21)`
  - `(3, 'John Doe', 'john@example.com', 22)`
- **Courses Data:**
  - `(1, 'Data Engineering', 4)`
  - `(2, 'Database Systems', 3)`
  - `(3, 'Machine Learning', 4)`
- **Enrollments Data:**
  - `[(1, 1, 'A'), (1, 2, 'B'), (2, 1, 'A'), (3, 3, 'C')]`

---

## 7. Sample Output
```text
Students with their enrolled courses:
Student: Ravi Kumar      | Course: Data Engineering    | Grade: A
Student: Ravi Kumar      | Course: Database Systems    | Grade: B
Student: Asha Sharma     | Course: Data Engineering    | Grade: A
Student: John Doe        | Course: Machine Learning    | Grade: C

Updated Student Record:
(1, 'Ravi Kumar', 'ravi@example.com', 23)

Enrollments after deleting Grade 'B':
(1, 1, 1, 'A')
(3, 2, 1, 'A')
(4, 3, 3, 'C')

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully constructed an ACID-compliant normalized relational database in SQLite, enforced entity and referential integrity constraints, and executed parameterized multi-table CRUD operations.

---

## 9. Learning Outcome
- Mastered relational data modeling, table constraints, and relational integrity.
- Learned efficient parameterized batch insertion using `executemany`.
- Understood multi-table join execution plans and query optimization.
- Built foundational relational database skills required for downstream analytical data warehouses.
