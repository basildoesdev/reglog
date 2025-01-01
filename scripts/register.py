import sqlite3
import hashlib

def register_user(username, password, email):
    try:
        conn = sqlite3.connect('../db/users.db')
        cursor = conn.cursor()

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert user into the database
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                       (username, hashed_password, email))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username or email already exists.")
    finally:
        conn.close()

# Example usage
username = input("Enter a username: ")
password = input("Enter a password: ")
email = input("Enter an email: ")
register_user(username, password, email)
