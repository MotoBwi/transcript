from flask import Flask, render_template, request, jsonify, redirect, session
import os
from transcribe import transcribe_audio
from ai_model import analyze_text
from email_notifications import send_email
from models import create_db, get_department_email, insert_transcription, validate_user, create_user
from flask import Flask, render_template, request, redirect, session, flash


app = Flask(__name__)
app.secret_key = 'd0c38d56fa99f546432e06aa0146b9f4527db5356c105377'

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
create_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate the user credentials
        if validate_user(username, password):  # Replace with your validation logic
            session['user'] = username
            return redirect('/')
        else:
            # Use Flask's flash mechanism to display the popup
            flash('Invalid credentials. Please try again.', 'error')
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            return jsonify({'status': 'success', 'message': 'User registered successfully'})
        else:
            return jsonify({'status': 'failure', 'message': 'Username already exists'})
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/inspect', methods=['POST'])
def inspect():
    if 'user' not in session:  # Ensure the user is logged in
        return redirect('/login')
    
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return "File type not allowed"

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Transcribe the audio file
    transcription = transcribe_audio(filename)

    # Analyze the transcription
    issue_category = analyze_text(transcription)

    # Get department email for notification
    department_email = get_department_email(issue_category)

    if department_email:
        send_email(issue_category, transcription, department_email)

    # Insert transcription data into the database
    username = session['user']  # Get the username from the session
    insert_transcription(username, transcription, f"Issue categorized as {issue_category}", "success")

    return jsonify({
        'status': 'success',
        'transcription': transcription,
        'category': issue_category
    })


if __name__ == '__main__':
    app.run(debug=True)
