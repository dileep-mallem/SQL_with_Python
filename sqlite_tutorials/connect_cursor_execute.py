import sqlite3

conn=sqlite3.connect("students.db")
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT)
""")

# 3. Insert example mock data
sample_students = [
    (1, "Alice Smith", "Computer Science"),
    (2, "Bob Jones", "Mechanical Engineering"),
    (3, "Charlie Brown", "Mathematics"),
    (4, "Diana Prince", "Physics")
]

# IGNORE ensures it won't crash if you run this script multiple times
cursor.executemany("""
INSERT OR IGNORE INTO students (id, name, department) 
VALUES (?, ?, ?)
""", sample_students)

# 4. Commit changes and close the connection
conn.commit()

print("Database 'students.db' successfully created and populated!")

# 5. Quick test: Read the data back to verify
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

print("\nCurrent Table Contents:")
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Department: {row[2]}")

conn.close()

