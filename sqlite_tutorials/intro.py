import sqlite3 
# SQL is not case-sensitive , just to read SQL things efficiently , we wrote SQL in Capital 

conn=sqlite3.connect("tutorial.db") # creates if not exits 
c=conn.cursor()

# A DB consists Tables , Tables consits of Data 
def create_table() : 
    c.execute('CREATE TABLE IF NOT EXISTS cinema(movieName TEXT UNIQUE , genre TEXT , BoxOffice REAL)')      # Cursor does all the executions of Things 
    # Table Created , UNIQUE does prevent Duplicate of Smae Data after Every Run 
def data_entry() : 
    c.execute("INSERT or IGNORE INTO cinema VALUES('Dune 3','SCI-FI',250)")
    conn.commit() # to Save , Anytime u modify in ur db , need to write conn.commit()
     
def display_table() :
    c.execute("SELECT * FROM cinema")
    c.close() # Close the Cursor
    conn.close() # Close the DB

create_table()
data_entry()
display_table()