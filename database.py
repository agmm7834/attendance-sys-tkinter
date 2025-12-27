import sqlite3

DB_NAME = "attendance.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_student(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM students")
    data = cur.fetchall()
    conn.close()
    return data

def mark_attendance(student_id, date, status):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
        (student_id, date, status)
    )
    conn.commit()
    conn.close()
