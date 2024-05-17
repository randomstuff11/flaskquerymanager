import sqlite3

def setup_database():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()

    # Create table for all queries
    c.execute('''
    CREATE TABLE IF NOT EXISTS all_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        connection_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Create table for saved queries
    c.execute('''
    CREATE TABLE IF NOT EXISTS saved_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        connection_id INTEGER
    )''')

    # Create table for connection details
    c.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        connection_string TEXT
    )''')

    conn.commit()
    conn.close()

setup_database()
