import sqlite3

# Connect to database (it will create file if not exists)
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    persons_detected INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")
