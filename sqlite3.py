import sqlite3

con = sqlite3.connect("clinic.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone TEXT
)
""")

con.commit()
con.close()
