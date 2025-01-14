import sqlite3
from flask import Flask, render_template, request, jsonify, redirect
import os
from transcribe import transcribe_audio  # Ensure this function handles transcription with Whisper
from ai_model import analyze_text       # Your AI model analysis function
from email_notifications import send_email  # Function to send email notifications
from models import create_db, get_department_email, insert_transcription  # SQLite database interaction

app = Flask(__name__)

# Configure the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database when the app starts
create_db()  # Ensure tables are created when the app starts

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inspect', methods=['POST'])
def inspect():
    # Check if the file part is in the request
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return redirect(request.url)

    # If the file is allowed, save it and process it
    if file and allowed_file(file.filename):
        # Save the file to the UPLOAD_FOLDER
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Transcribe the audio file
        transcription = transcribe_audio(filename)
        
        # Analyze the transcription using AI
        issue_category = analyze_text(transcription)
        
        # Get department email for notification
        department_name = issue_category  # Assuming the issue category is the department name
        email = get_department_email(department_name)
        
        if email:
            # Send email notification to the department
            send_email(issue_category, transcription, email)
        
        # Insert transcription into the database
        message = f"Issue categorized as {issue_category} and notified."
        status = "success"
        insert_transcription(transcription, message, status)
        
        # Return the transcription and issue category as a response
        return jsonify({
            'status': 'success',
            'message': message,
            'transcription': transcription
        })

    return "File type not allowed"

if __name__ == '__main__':
    app.run(debug=True)
