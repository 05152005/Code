import sqlite3
import os

# DATABASE PATH (same folder as your project)
DB_PATH = os.path.join(os.path.dirname(__file__), "people.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # CREATE TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            purpose TEXT NOT NULL,
            document TEXT NOT NULL,
            datetime TEXT NOT NULL
        )
    """)

    # OPTIONAL: INSERT SAMPLE DATA (only if empty)
    cursor.execute("SELECT COUNT(*) FROM people")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_data = [
            ("Cyrill", "09123456789", "Cedula", "Community Tax Certificate", "2026-01-01"),
            ("Maria", "09987654321", "Job", "Barangay Clearance", "2026-01-02"),
            ("Juan", "09876543210", "Permit", "Business Permit", "2026-01-03"),
            ("Ana", "09111111111", "School", "Barangay ID", "2026-01-04"),
            ("Pedro", "09222222222", "Travel", "Residency Certificate", "2026-01-05"),
        ]

        cursor.executemany("""
            INSERT INTO people (name, contact, purpose, document, datetime)
            VALUES (?, ?, ?, ?, ?)
        """, sample_data)

        print("✅ Sample data inserted!")

    conn.commit()
    conn.close()

    print("✅ Database ready: people.db")


# RUN THIS FILE FIRST
if __name__ == "__main__":
    init_db()