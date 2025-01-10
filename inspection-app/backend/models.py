import sqlite3

# SQLite database file
DATABASE = 'inspection.db'

# Function to create the SQLite database and tables
def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create 'departments' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Function to get a user from the database
def get_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {'id': user[0], 'username': user[1], 'password': user[2]}
    return None

# Function to add a user to the database
def add_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        print(f"User '{username}' already exists. Skipping insertion.")
    else:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print(f"User '{username}' added successfully.")

    conn.close()

# Function to get a department email from the database
def get_department_email(department_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM departments WHERE name = ?', (department_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None

# Initialize the database and add a test user
if __name__ == "__main__":
    create_db()
    add_user('testuser', 'testpassword')  # Add a test user

import sqlite3

# Function to create the database and table
def create_db():
    conn = sqlite3.connect('inspection.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to get user details by username
def get_user(username):
    conn = sqlite3.connect('inspection.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'username': user[1], 'password': user[2]}
    return None
