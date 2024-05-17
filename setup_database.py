import sqlite3

def setup_database():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        connection_string TEXT NOT NULL,
        description TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        query_text TEXT NOT NULL,
        connection_id INTEGER,
        FOREIGN KEY (connection_id) REFERENCES connections(id)
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS query_sequences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        connection_id INTEGER,
        queries TEXT,  -- JSON array of queries
        FOREIGN KEY (connection_id) REFERENCES connections(id)
    )''')
    
    connection.commit()
    connection.close()

if __name__ == '__main__':
    setup_database()
