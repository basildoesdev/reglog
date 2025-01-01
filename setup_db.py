import sqlite3

# Establish connection
conn = sqlite3.connect('./db/users.db')  # This will create a SQLite file called 'users.db'
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

print("Database and table created successfully.")

# Commit and close
conn.commit()
conn.close()
