import sqlite3
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename
import os
from werkzeug.utils import secure_filename

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
    # Create users table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        name TEXT,
                        surname TEXT,
                        department TEXT,
                        post TEXT,
                        profile_picture TEXT)''')
    
    conn.commit()
    
    # Create the 'transcriptions' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            user TEXT NOT NULL,                        
            transcription TEXT NOT NULL,               
            message TEXT NOT NULL,                     
            status TEXT NOT NULL,                      
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP 
        )
    ''')

    # Create the 'email_notifications' table for email log details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,                    
            department TEXT NOT NULL,                   
            email_id TEXT NOT NULL,                     
            message TEXT NOT NULL,                      
            subject TEXT NOT NULL,                      
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP 
        )
    ''')

    conn.commit()
    conn.close()

# Function to get email notification details
def get_email_notification_details(user, department):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # SQL query to retrieve the latest email notification for a specific user and department
    cursor.execute('''
        SELECT subject, email_id, message, timestamp
        FROM email_notifications
        WHERE user_name = ? AND department = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (user, department))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'subject': result[0],
            'email': result[1],
            'message': result[2],
            'timestamp': result[3]
        }
    else:
        return None

# Insert email notification details into the database
def insert_email_notification(user, department_name, email, message, subject, timestamp):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = '''
    INSERT INTO email_notifications (user_name, department, email_id, message, subject, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    
    cursor.execute(query, (user, department_name, email, message, subject, timestamp))
    conn.commit()
    conn.close()

# Function to get department email
def get_department_email(department_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM departments WHERE name = ?', (department_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Function to insert transcription data
def insert_transcription(transcription, message, status, user):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO transcriptions (transcription, message, status, user)
        VALUES (?, ?, ?, ?)
    ''', (transcription, message, status, user))

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

# Function to get the current timestamp in IST
def get_ist_timestamp():
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(india_timezone)
    return current_time.strftime('%Y-%m-%d %H:%M:%S')

# Function to get user info
def get_user_info(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname, department, post, profile_picture FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            'name': user[0],
            'surname': user[1],
            'department': user[2],
            'post': user[3],
            'profile_picture': user[4] or 'default_picture.jpg'  
        }
    else:
        return None

# Function to update user information
def update_user_info(username, name, surname, department, post, profile_picture):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # If a new profile picture was uploaded, save it in the uploads folder
    profile_picture_filename = None
    if profile_picture and isinstance(profile_picture, str) == False:  # Ensure it's a file object
        # Ensure the filename is secure and save it to the 'uploads' folder
        profile_picture_filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join('uploads', profile_picture_filename))
    else:
        # If no new profile picture, use the current one or default
        profile_picture_filename = profile_picture if profile_picture else 'default_picture.jpg'

    # SQL query to update user information
    cursor.execute("""
        UPDATE users
        SET name = ?, surname = ?, department = ?, post = ?, profile_picture = ?
        WHERE username = ?
    """, (name, surname, department, post, profile_picture_filename, username))

    connection.commit()
    connection.close()

