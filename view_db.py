import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM attendance").fetchall()

for row in rows:
    print(row)

conn.close()
