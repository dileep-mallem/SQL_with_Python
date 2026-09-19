import sqlite3 

# Create Tabel - Define Schema 
with sqlite3.connect("school.db") as conn : 
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INTEGER PRIMARY KEY AUTOINCREMENT ,
            name TEXT NOT NULL ,
            email TEXT UNIQUE NOT NULL ,
            dept TEXT DEFAULT 'CS',
            year INTEGER CHECK(year BETWEEN 1 AND 4)
        );
        CREATE TABLE IF NOT EXISTS courses(
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT DEFAULT NULL,
            credits INTEGER DEFAULT 3,
            dept TEXT
        );

    """)
# Insert - SIngle Row and Batch INSERT s
with sqlite3.connect("school.db") as conn : 
    c=conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO students(name, email , dept , year) VALUES (?,?,?,?)", # SQLite compiles the query layout first using the ? symbols. It keeps the SQL command completely separate from your data.
        ("Dileep Kumar","mailtodileepmallem@gmail.com","AIML",2)
    )
    student_id=c.lastrowid  # get auto-generated PK
    print(f"Inserted student ID: {student_id}")

    # Batch INSERT 
    more_students=[
        ("Rhaneyra T","queenofsevenkingdoms@gmail.com","CS",3),
        ("DAEMON T","rougeprince@gmail.com","CS",3),
        ("Jon SNow ","lordcommanderofnightswatch@gmail.com","EE",2)

    ]

    c.executemany(
        "INSERT OR IGNORE INTO students (name,email,dept,year) VALUES (?,?,?,?)", # You can omit the column names (name, email, dept, year) if you are providing values for every single column in the exact order they were created.
        more_students
    )