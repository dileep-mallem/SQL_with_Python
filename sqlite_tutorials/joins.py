import sqlite3 

conn=sqlite3.connect("sqlite_tutorials/up_del.db")


# Joins 
# Innner Join ->Return  Only rows eith matching keys in both tables 
# left Join -> returns All left rows + match right (NULL if not match)
# cross join -> returns EVERY combination of rows from both tables 
# self join -> Table joined with itself 

def inner_join() : 
    conn.row_factory = sqlite3.Row
    c=conn.cursor()
    c.execute("""
        SELECT s.name,
            c.course_name,
            e.grade 
        FROM students s 
            INNER JOIN enrollments e ON s.student_id = e.student_id 
            INNER JOIN courses c ON e.course_id = c.course_id 
        ORDER BY s.name , c.course_name 
        """)

    for row in c.fetchall() : 
        print(f"{row['name']:20} | {row['course_name']:25} | {row['grade']}")
inner_join()

# DAEMON T             | Database Management Systems | 6.5
# Dileep Kumar         | Data Structures and Algorithms | 8.8
# Dileep Kumar         | Machine Learning          | 9.5
# Jon SNow             | Introduction to Python    | 8.2
# Rhaneyra T           | Data Structures and Algorithms | 7.5
# Rhaneyra T           | Database Management Systems | 9.0