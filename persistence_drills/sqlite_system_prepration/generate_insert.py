# generate_inserts.py

file_path = "inserts.sql"

with open(file_path, "w") as f:
    for i in range(2, 502):  # Starting from 2, since 1 is already inserted
        company_name = f"Company_{i}"
        insert_stmt = f"INSERT INTO COMPANIES VALUES ('{company_name}', {i});\n"
        f.write(insert_stmt)

print(f"{file_path} created with 500 insert statements.")
