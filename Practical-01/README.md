# Practical-01: Semi-Structured & Unstructured Data Parsing, Binary Serialization, Regular Expressions, and SQL CRUD

---

## 1. Aim
To ingest, parse, validate, and manipulate diverse data representations—including unstructured text, semi-structured formats (CSV, HTML, XML, JSON), fixed-width binary records via low-level memory structs, pattern tokenization using regular expressions, and relational database schema design with full SQL CRUD capabilities in SQLite.

---

## 2. Theory

### 2.1 Data Classification & Parsing Mechanics
In enterprise data engineering pipelines, raw data arrives in three fundamental categories:
1. **Unstructured Data (Text):** Unordered streams of characters lacking a predefined data model. Parsing requires custom tokenization, delimiter extraction, and line-by-line validation.
2. **Semi-Structured Data:** Self-describing data containing markers or tags separating semantic elements:
   - **CSV (Comma-Separated Values):** Delimited tabular format parsed via Python's built-in `csv` module with dialect handling.
   - **JSON (JavaScript Object Notation):** Lightweight key-value hierarchies serialized as nested objects and arrays.
   - **XML (Extensible Markup Language):** Tree-structured hierarchical documents parsed via DOM or event-driven stream parsing (`xml.etree.ElementTree`).
   - **HTML (HyperText Markup Language):** Document structure parsed via state-machine event handlers using Python's `html.parser.HTMLParser`.
3. **Structured Binary Data:** Packed byte streams matching physical memory representations. Serializing data using Python's `struct` module enables fixed-byte efficiency, eliminating text overhead and ensuring rapid I/O serialization.

### 2.2 Regular Expressions in Data Quality
Regular expressions (`re`) define formal search patterns using deterministic finite automata (DFA). In data preprocessing, regex ensures:
- Token validation against strict domain definitions (e.g., standard email compliance, strict phone number formats).
- Non-destructive token extraction (`re.search`, `re.findall`, `re.finditer`).
- Privacy masking and text normalization (`re.sub`).

### 2.3 Relational Schema Design & ACID Properties
Relational databases enforce structural consistency via schema constraints (Primary Keys, Foreign Keys, Unique indices). SQLite provides ACID-compliant (Atomicity, Consistency, Isolation, Durability) transaction semantics. Enforcing `ON DELETE CASCADE` guarantees referential integrity across parent-child table associations.

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Standard Libraries:** `csv`, `json`, `xml.etree.ElementTree`, `html.parser`, `struct`, `re`, `sqlite3`, `os`
- **Environment:** Jupyter Notebook / Google Colab / Local Terminal

---

## 4. Procedure
1. **Task 1: Multi-Format Data Parsing (`Data_Parsing.ipynb`)**
   - Extract raw text lines; tokenize fields by delimiters; filter malformed lines and detect impossible numerical values (e.g., Age $> 120$ or Age missing).
   - Read CSV files using `csv.reader`, handle headers, validate field count, and verify numerical data types.
   - Implement custom `HTMLTableParser` by subclassing `HTMLParser` to dynamically extract tabular table cells (`<td>`, `<tr>`).
   - Parse XML trees with `xml.etree.ElementTree`, traverse student nodes, and extract nested attributes.
   - Decode JSON payloads with `json.loads` and validate required keys.
2. **Task 2: Binary File Operations (`Binary_File_Operations.ipynb`)**
   - Define a fixed-record struct format `<i10sf` (Little-endian: 4-byte integer ID, 10-byte byte string for Name, 4-byte float for Marks = 18 bytes/record).
   - Pack structured tuples and write to `students.bin` in binary write mode (`wb`).
   - Read binary records in chunks of 18 bytes using `f.read(RECORD.size)` and unpack using `RECORD.unpack()`.
3. **Task 3: Regular Expressions (`Regex_Operations.ipynb`)**
   - Execute regex search and findall for phone numbers (`\d{5}-\d{5}`), emails (`[\w.+-]+@[\w-]+(?:\.[\w-]+)+`), and ISO/custom dates.
   - Split irregular delimited text using `re.split(r"[,;|	]+", text)`.
   - Redact sensitive telephone numbers using `re.sub()`.
4. **Task 4: Relational Database & SQL CRUD (`SQL_CRUD.ipynb`)**
   - Create SQLite database with relational tables: `departments`, `students`, `courses`, and `enrollments`.
   - Configure foreign keys with `ON DELETE CASCADE`.
   - Execute SQL CRUD: Create tables, Insert records, Read using multi-table `JOIN`, Update records, and Delete parent records to test cascading deletion.

---

## 5. Code Explanation

### Task 1: Multi-Format Parser
```python
# Custom HTML table parser subclassing standard HTMLParser
class HTMLTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.current_row, self.in_cell = [], [], False
    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"): self.in_cell = True
    def handle_endtag(self, tag):
        if tag in ("td", "th"): self.in_cell = False
        elif tag == "tr" and self.current_row:
            self.rows.append(self.current_row)
            self.current_row = []
    def handle_data(self, data):
        if self.in_cell and data.strip():
            self.current_row.append(data.strip())
```

### Task 2: Binary Struct Packing
```python
import struct
# Format: < (little-endian), i (int32), 10s (10-char string), f (float32)
RECORD = struct.Struct("<i10sf")
with open("students.bin", "wb") as f:
    for sid, name, marks in students:
        f.write(RECORD.pack(sid, name.encode().ljust(10, b"\0"), marks))
```

### Task 3: Regex Pattern Matching
```python
# Email and phone pattern extraction
emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
phones = re.findall(r"\b\d{5}-\d{5}\b", text)
masked_text = re.sub(r"\b\d{5}-\d{5}\b", "[REDACTED]", text)
```

### Task 4: Relational Schema & Cascading Deletes
```python
cur.execute("""
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id  INTEGER,
    grade      TEXT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
""")
```

---

## 6. Sample Input
- **Sample Text:**
  ```text
  Name: Asha, Age: 21, City: Pune
  Name: Ravi, Age: , City: Delhi
  Name: Meena, Age: 250, City: Chennai
  Bad line without fields
  ```
- **Binary Records Tuple:**
  ```python
  [(1, "Asha", 88.5), (2, "Ravi", 72.0), (3, "Meena", 95.25)]
  ```

---

## 7. Sample Output
```text
=== TASK 1: PARSING RESULTS ===
Text parsed: 2 valid records, 1 missing age, 1 out-of-range age (250)
CSV parsed: 3 records successfully loaded
XML parsed: 3 students extracted, average marks: 85.25
HTML table parsed: 3 rows successfully retrieved

=== TASK 2: BINARY STRUCT ===
Written students.bin: 54 bytes (18 bytes per record)
Unpacked record 1: ID=1, Name=Asha, Marks=88.5
Unpacked record 2: ID=2, Name=Ravi, Marks=72.0
Unpacked record 3: ID=3, Name=Meena, Marks=95.25

=== TASK 3: REGEX OPERATIONS ===
First phone (search): 98765-43210
Emails (findall)    : ['asha@mail.com', 'ravi_k@college.edu.in']
Redacted text       : Contact Asha at asha@mail.com or [REDACTED].

=== TASK 4: RELATIONAL CRUD ===
Tables created: departments, students, courses, enrollments
Rows deleted: 1 (cascading enrollments automatically purged)
Submitted by: Mohammad Ayaan Sajid Shaikh
```

---

## 8. Result
Successfully parsed raw text, CSV, XML, HTML, and JSON data formats; achieved bit-level binary serialization using `struct`; validated tokens using regular expressions; and demonstrated relational integrity and cascading CRUD queries in SQLite.

---

## 9. Learning Outcome
- Gained hands-on proficiency in ingesting and sanitizing diverse semi-structured data formats without third-party dependencies.
- Understood the performance benefits and storage efficiency of binary fixed-width packing over textual data.
- Mastered regular expression pattern construction for data auditing, validation, and redaction.
- Applied normalized relational modeling concepts and referential integrity constraints in transactional SQL engines.
