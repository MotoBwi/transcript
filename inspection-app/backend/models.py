import sqlite3

DATABASE = 'inspection_system.db'

# Function to create the SQLite database and table
def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the 'departments' table (if it doesn't already exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create the 'transcriptions' table (if it doesn't already exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcription TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Function to get department email from the database
def get_department_email(department_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query the department email from the database
    cursor.execute('SELECT email FROM departments WHERE name = ?', (department_name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None  # Return None if no department is found

# Function to insert transcription data into the database
def insert_transcription(transcription, message, status):
    conn = sqlite3.connect(DATABASE)  # Connect to the database
    cursor = conn.cursor()

    # SQL command to insert data into the transcriptions table
    cursor.execute('''
        INSERT INTO transcriptions (transcription, message, status)
        VALUES (?, ?, ?)
    ''', (transcription, message, status))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
