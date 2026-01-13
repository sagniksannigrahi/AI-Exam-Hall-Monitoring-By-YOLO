from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM attendance").fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_attendance()
    return render_template("index.html", attendance=data)

if __name__ == '__main__':
    app.run(debug=True)
