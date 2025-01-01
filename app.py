import os
from flask import Flask, request, jsonify,  render_template
import sqlite3
import hashlib

app = Flask(__name__)

# Register endpoint

DB_PATH = 'db/users.db'

# Ensure the database and table are created
def initialize_db():
    if not os.path.exists('db'):
        os.makedirs('db')  # Create the 'db' directory if it doesn't exist

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the 'users' table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database at app startup
initialize_db()

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = sqlite3.connect('./db/users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                       (username, hashed_password, email))
        conn.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists."}), 400
    finally:
        conn.close()

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, hashed_password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful!"}), 200
    else:
        try:
            conn.close()
        finally:
            return jsonify({"error": "Invalid username or password."}), 401
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
