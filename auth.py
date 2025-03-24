import sqlite3
import re
from getpass import getpass

# Database connection
DATABASE_PATH = "database/users.db"

def create_users_table():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        security_question TEXT,
        security_answer TEXT
    )
    """)
    connection.commit()
    connection.close()

def register_user():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("\n--- Register ---")
    username = input("Enter a username: ")

    # Password Validation
    while True:
        password = getpass("Enter a password: ")
        if not validate_password_strength(password):
            print("Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, one number, and one special character.")
            continue
        confirm_password = getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Try again.")
            continue
        break

    # Optional: Add security question
    security_question = input("Enter a security question (e.g., 'What is your favorite color?'): ")
    security_answer = input("Enter the answer: ")

    try:
        cursor.execute("INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
                       (username, password, security_question, security_answer))
        connection.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try a different one.")
    finally:
        connection.close()

def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def login_user():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome back, {username}!")
    else:
        print("Invalid username or password.")

    connection.close()

def forgot_password():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("\n--- Forgot Password ---")
    username = input("Enter your username: ")

    cursor.execute("SELECT security_question, security_answer FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        security_question, correct_answer = user
        print(f"Security Question: {security_question}")
        answer = input("Your Answer: ")

        if answer == correct_answer:
            while True:
                new_password = getpass("Enter a new password: ")
                if not validate_password_strength(new_password):
                    print("Password must meet strength requirements. Try again.")
                    continue
                confirm_password = getpass("Confirm new password: ")
                if new_password != confirm_password:
                    print("Passwords do not match. Try again.")
                    continue
                break

            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
            connection.commit()
            print("Password updated successfully!")
        else:
            print("Incorrect answer. Cannot reset password.")
    else:
        print("Username not found.")

    connection.close()

if __name__ == "__main__":
    create_users_table()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


