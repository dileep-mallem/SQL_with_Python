import sqlite3 


with sqlite3.connect("sqlite_tutorials/up_del.db") as conn : 
    conn.row_factory = sqlite3.Row # Access Cols by name 
    c=conn.cursor()


    # Basic Select 
    c.execute("SELECT * FROM students")
    for row in c.fetchall() : 
        print(row["name"],row["dept"]) # dic-style 
        # Dileep Kumar AIML
        # Rhaneyra T CS
        # DAEMON T CS
        # Jon SNow  EE

    # WHERE with op's 
    c.execute("""
        SELECT name,dept,year
        FROM students
        WHERE dept IN ('CS','AI')
            AND year BETWEEN 2 AND 3 
            AND name LIKE 'D%'
        ORDER BY year DESC , name ASC -- order by  for Asc or Des Order 
        LIMIT 10 

    """)
    # Using name place holders 
    c.execute(
        "SELECT * FROM students WHERE dept = :dept AND year = :year",
        {"dept":"CS","year":2}
    )





