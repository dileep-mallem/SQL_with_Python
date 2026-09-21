import sqlite3 

conn=sqlite3.connect("sqlite_tutorials/up_del.db")
c=conn.cursor()


def create_table() : 
     conn.executescript("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id    INTEGER NOT NULL,
            course_id     INTEGER NOT NULL,
            grade         REAL    CHECK(grade BETWEEN 0.0 AND 10.0),
            enrolled_date TEXT    DEFAULT (DATE('now')),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
                ON DELETE CASCADE,
            FOREIGN KEY (course_id)  REFERENCES courses(course_id),
            UNIQUE (student_id, course_id)   -- no duplicate enrollments
        );
    """)

def update() : 
     # ── UPDATE with CASE (conditional) ────────────────────────
    c.execute("""
        UPDATE enrollments
        SET grade = grade + 0.5
        WHERE student_id IN (
            SELECT student_id FROM students WHERE dept = 'AI'
        )
        AND grade < 9.5
    """)
    conn.commit()

def delete() : 
    #  DELETE with subquery 
    c.execute("""
        DELETE FROM enrollments
        WHERE student_id NOT IN (SELECT student_id FROM students)
    """)    
    conn.commit()                              # clean up orphaned enrollments

create_table()
update()


# Sample enrollment records: (student_id, course_id, grade)
# Note: enrolled_date will automatically use the default DATE('now')
enrollment_data = [
    (1, 1, 9.5),  # Dileep Kumar -> Machine Learning
    (1, 2, 8.8),  # Dileep Kumar -> Data Structures
    (2, 2, 7.5),  # Rhaneyra T   -> Data Structures
    (2, 3, 9.0),  # Rhaneyra T   -> Database Management
    (3, 3, 6.5),  # DAEMON T     -> Database Management
    (4, 5, 8.2),  # Jon Snow     -> Introduction to Python
]

def insert_enrollments():
    with sqlite3.connect("sqlite_tutorials/up_del.db") as conn:
        c = conn.cursor()
        
        # Enforce foreign key constraints in SQLite
        c.execute("PRAGMA foreign_keys = ON;")
        
        try:
            # Using INSERT OR IGNORE to handle the UNIQUE(student_id, course_id) constraint safely
            c.executemany("""
                INSERT OR IGNORE INTO enrollments (student_id, course_id, grade) 
                VALUES (?, ?, ?);
            """, enrollment_data)
            
            conn.commit()
            print(f"Successfully inserted {c.rowcount} enrollment records.")
            
        except sqlite3.IntegrityError as e:
            print(f"Foreign Key or Check Constraint violation: {e}")


insert_enrollments()


