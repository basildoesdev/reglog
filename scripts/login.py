import sqlite3
import hashlib

def login_user(username, password):
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()

    # Hash the input password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Verify the user
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, hashed_password))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

    conn.close()

# Example usage
username = input("Enter your username: ")
password = input("Enter your password: ")
login_user(username, password)
