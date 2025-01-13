import sqlite3

DATABASE = 'inspection_system.db'

# Function to create the SQLite database and tables
def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the 'departments' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create the 'transcriptions' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            user TEXT NOT NULL,                        -- Stores the username of the uploader
            transcription TEXT NOT NULL,               -- Stores the transcription text
            message TEXT NOT NULL,                     -- Status message of the transcription
            status TEXT NOT NULL,                      -- Status of the operation (e.g., success, failure)
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Automatic timestamp
        )
    ''')

    # Create the 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Function to get department email from the database
def get_department_email(department_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM departments WHERE name = ?', (department_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Function to insert transcription data
def insert_transcription(username, transcription, message, status):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transcriptions (user, transcription, message, status)
        VALUES (?, ?, ?, ?)
    ''', (username, transcription, message, status))
    conn.commit()
    conn.close()

# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to create a new user
def create_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
