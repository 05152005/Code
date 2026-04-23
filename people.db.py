import sqlite3

conn = sqlite3.connect("people (12).db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT,
    purpose TEXT,
    document TEXT,
    datetime TEXT
)
""")

# optional test data
cursor.execute("INSERT INTO people (name, contact, purpose, document, datetime) VALUES ('Cyrill', '09123', 'Cedula', 'Cedula', '2026')")
cursor.execute("INSERT INTO people (name, contact, purpose, document, datetime) VALUES ('Maria', '09123', 'Job', 'Brgy ID', '2026')")
cursor.execute("INSERT INTO people (name, contact, purpose, document, datetime) VALUES ('Juan', '09123', 'Permit', 'Permit', '2026')")

conn.commit()
conn.close()

print("Database and table created!")