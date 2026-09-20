import sqlite3 


conn=sqlite3.connect("up_del.db")
c=conn.cursor()

# Create Tabel - Define Schema 
with sqlite3.connect("up_del.db") as conn : 
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
            dept TEXT,
            UNIQUE(course_name, dept) -- Prevents duplicate courses in the same department
        );

    """)
# Insert - SIngle Row and Batch INSERT s
with sqlite3.connect("up_del.db") as conn : 
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

# Add columns 
def add_col(): 
    try:
        c.execute("ALTER TABLE students ADD COLUMN grade REAL;")
        print("Column Grade added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'grade' already exists. Skipping column creation.")
        else:
            raise e

# Insert Values in Grade Col 
def insert_data() : 
    c.execute("UPDATE students SET grade = 9.85 WHERE student_id = 1;")
    c.execute("UPDATE students SET grade = 8.0 WHERE student_id = 2;")
    c.execute("UPDATE students SET grade = 7.0 WHERE student_id = 3;")
    c.execute("UPDATE students SET grade = 6.0 WHERE student_id = 4;")

        # Update all 4 students records in  single line
        # c.execute("""
        #     UPDATE students SET grade = CASE student_id 
        #         WHEN 1 THEN 9.85 
        #         WHEN 2 THEN 8.0 
        #         WHEN 3 THEN 7.0 
        #         WHEN 4 THEN 6.0 
        #     END WHERE student_id IN (1, 2, 3, 4);
        # """)
    conn.commit()
    print("Grades updated for existing students.")
    

# Update 

def update_data() : 
    c.execute("UPDATE students SET year=? WHERE email=?",
              (3,"mailtodileepmallem@gmail.com")
              )
    
    conn.commit()
     # UPDATE with CASE (conditional)

    c.execute("""
        UPDATE students 
        SET grade = grade + 0.5 
        WHERE student_id IN(
            SELECT student_id FROM students WHERE dept='CS'
            )
        AND grade < 9.5
     """)
    conn.commit()
    print(f"Rows Updated : {c.rowcount}")
    print("Grade Col Updated ")
    

add_col()
insert_data()
update_data()


single_course=("Machine Learning", "Dr. Andrew Ng", 4, "AIML")

more_courses = [
    ("Data Structures and Algorithms", "Prof. Charles Leiserson", 4, "CS"),
    ("Database Management Systems", "Dr. Raghu Ramakrishnan", 3, "CS"),
    ("Basic Electrical Engineering", "Prof. Alexander Sadiku", 3, "EE"),
    ("Introduction to Python", None, 2, "CS") # Testing the DEFAULT NULL constraint
]

def insert_courses():
    
    c.execute(
        "INSERT OR IGNORE INTO courses (course_name, instructor, credits, dept) VALUES (?, ?, ?, ?)",
        single_course
    )
    print(f"Inserted single course. ID: {c.lastrowid}")

    #  Batch Row Insertion
    c.executemany(
        "INSERT OR IGNORE INTO courses (course_name, instructor, credits, dept) VALUES (?, ?, ?, ?)",
        more_courses
    )
    print(f"Successfully batch inserted {c.rowcount} courses.")
    
    # Commit changes to the database
    conn.commit()

insert_courses()

def delete_data() : 
    c.execute("DELETE FROM students WHERE student_id=?",
              (5,)
    )
    
    c.execute("DELETE FROM courses WHERE course_id=?",
              (4,)
    ) 
    # Delete with SubQuery 
    # Subquery finds all departments that exist in the students table.
    # The main query deletes courses whose department is NOT in that list.
    c.execute("""
        DELETE FROM courses 
            WHERE dept NOT IN(
            SELECT DISTINCT dept
            FROM students   
            WHERE dept IS NOT NULL
        );
    """)
    conn.commit()

    print("Delte Single aand with SubQueires Succefully")

delete_data()
