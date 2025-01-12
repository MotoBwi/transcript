from flask import Flask, render_template, request, jsonify, redirect, session, flash
import os
from datetime import datetime
import pytz
from werkzeug.utils import secure_filename
from models import create_db, get_user_info, update_user_info, validate_user
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = 'd0c38d56fa99f546432e06aa0146b9f4527db5356c105377'

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'ogg', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the database
create_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to get the current time in IST (Indian Standard Time)
def get_indian_time():
    indian_timezone = pytz.timezone("Asia/Kolkata")
    indian_time = datetime.now(indian_timezone)
    return indian_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    user_info = get_user_info(session['user'])
    
    if not user_info:
        flash('User info not found.', 'error')
        return redirect('/login')

    return render_template('index.html', user_info=user_info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if validate_user(username, password):
            session['user'] = username
            return redirect('/')
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect('/login')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect('/login')

    # Get the user info
    user_info = get_user_info(session['user'])

    if request.method == 'POST':
        # Handle profile update (name, surname, department, post)
        name = request.form['name']
        surname = request.form['surname']
        department = request.form['department']
        post = request.form['post']
        profile_picture = request.files.get('profile_picture')  # Get new profile picture

        # If a profile picture is uploaded, save it
        if profile_picture:
            # Save the profile picture and get the filename path
            profile_picture_filename = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename)
            profile_picture.save(profile_picture_filename)
        else:
            # If no new profile picture, use the current one
            profile_picture_filename = user_info['profile_picture']

        # Update the user's info in the database
        update_user_info(session['user'], name, surname, department, post, profile_picture_filename)

        flash('Profile updated successfully!', 'success')
        return redirect('/profile')

    return render_template('profile.html', user_info=user_info)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'profile_picture' not in request.files:
        return 'No file part'
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    
# Serve files from the 'uploads' folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


if __name__ == '__main__':
    app.run(debug=True)
