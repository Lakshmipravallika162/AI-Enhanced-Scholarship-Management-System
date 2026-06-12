"""
Database Module - SQLite with all tables
Tables: users, applications, predictions, reports
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "scholarship.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table (students + admins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            role        TEXT    DEFAULT 'student',   -- 'student' | 'admin'
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Scholarship Applications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id                 INTEGER NOT NULL,
            gpa                     REAL    NOT NULL,
            attendance_pct          INTEGER NOT NULL,
            family_income_level     TEXT    NOT NULL,
            previous_scholarship    INTEGER DEFAULT 0,
            extracurricular_score   INTEGER DEFAULT 0,
            category_eligible       INTEGER DEFAULT 0,
            status                  TEXT    DEFAULT 'Pending',  -- Pending|Approved|Rejected
            submitted_at            TEXT    DEFAULT (datetime('now')),
            reviewed_at             TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ML Predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id  INTEGER NOT NULL,
            result          TEXT    NOT NULL,   -- Eligible | Not Eligible
            probability     REAL    NOT NULL,
            predicted_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(application_id) REFERENCES applications(id)
        )
    """)

    # GenAI Reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id  INTEGER NOT NULL,
            report_text     TEXT    NOT NULL,
            generated_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY(application_id) REFERENCES applications(id)
        )
    """)

    # Seed default admin
    cursor.execute("""
        INSERT OR IGNORE INTO users (name, email, password, role)
        VALUES ('Admin Officer', 'admin@scholarship.com', 'admin123', 'admin')
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized.")
