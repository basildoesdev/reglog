from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Register endpoint

@app.route('/')
def home():
     return '''
    <html>
        <head><title>Welcome</title></head>
        <body>
            <h1>Welcome to the Registration and Login Portal!</h1>
            <p>Use the API endpoints for registration and login.</p>
        </body>
    </html>
    '''

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
