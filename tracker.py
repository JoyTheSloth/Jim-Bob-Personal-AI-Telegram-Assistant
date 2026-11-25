import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "applications.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            recipient_email TEXT,
            role_type TEXT,
            subject TEXT,
            resume_file TEXT,
            timestamp DATETIME,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_application(company: str, recipient_email: str, role_type: str, subject: str, resume_file: str, status: str = "Sent"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, recipient_email, role_type, subject, resume_file, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, recipient_email, role_type, subject, resume_file, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status))
    conn.commit()
    conn.close()

def get_recent_applications(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, recipient_email, role_type, timestamp, status FROM applications ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT company) FROM applications")
    total, companies = cursor.fetchone()
    conn.close()
    return total, companies

def check_applied(query: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    q = f"%{query.strip().lower()}%"
    cursor.execute("""
        SELECT company, recipient_email, role_type, timestamp, status 
        FROM applications 
        WHERE LOWER(company) LIKE ? OR LOWER(recipient_email) LIKE ?
        ORDER BY id DESC LIMIT 5
    """, (q, q))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
