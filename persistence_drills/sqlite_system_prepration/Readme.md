# SQLite System Preparation
This guide explains how to set up SQLite locally, create a test database, insert data, and verify results.
All work is done in the following folder:
```
D:\aganitha\_bootcamp\persistence\_drills\sqlite\_system\_prepration
```
## :hammer_and_spanner: Prerequisites
- SQLite3 must be installed on your system.
- Python 3 must be installed to generate insert SQL file.
To check:
```bash
sqlite3 --version
python --version
```
## :file_folder: Step-by-Step Instructions
### :white_tick: 1. Navigate to Project Folder
Open **Command Prompt** and run:
```bash
cd /d D:\aganitha_bootcamp\persistence_drills\sqlite_system_prepration
```
---
### :white_tick: 2. Create the SQLite Database
Run the following command to create and open a new SQLite database:
```bash
sqlite3 example.db
```
Then in the SQLite shell, run:
```sql
CREATE TABLE COMPANIES (company_name VARCHAR(20), id INT);
INSERT INTO COMPANIES VALUES ('aganitha', 1);
.exit
```
This creates a database file named `example.db` with one record.
---
### :white_tick: 3. Generate 500 Insert Statements
Create a Python file `generate_inserts.py` with the following content:
```python
# generate_inserts.py
file_path = "inserts.sql"
with open(file_path, "w") as f:
    for i in range(2, 502):  # Starting from 2
        company_name = f"Company_{i}"
        f.write(f"INSERT INTO COMPANIES VALUES ('{company_name}', {i});\n")
print(f"{file_path} created with 500 insert statements.")
```
Run this script from command prompt:
```bash
python generate_inserts.py
```
It will generate a file `inserts.sql` in the same folder.
---
### :white_tick: 4. Apply Insert Statements to the Database
Run:
```bash
sqlite3 example.db < inserts.sql
```
---
### :white_tick: 5. Verify the Data
Open the database again:
```bash
sqlite3 example.db
```
Then run inside the SQLite shell:
```sql
SELECT COUNT(*) FROM COMPANIES;
```
Expected output:
```
501
```
---
#### Terminal - Steps
![Terminal Overview](/persistence_drills/sqlite_system_prepration/records_insertions.png)
---
## :bulb: Notes
* SQLite does **not** require a server. The database is just a single file (`example.db`) you can copy anywhere.
* You can use **DB Browser for SQLite** or open the DB inside **VS Code** or **PyCharm** with a plugin for visual browsing.