from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from models import create_db, get_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize the database
create_db()

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user(user_id)  # Fetch user data from the database
    if user_data:
        return User(id=user_data['id'], username=user_data['username'])
    return None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database and verify credentials
    conn = sqlite3.connect('inspection.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Valid credentials
        session['username'] = username
        login_user(User(id=user[0], username=user[1]))  # Log the user in using Flask-Login
        flash('Login successful!', 'success')
        return redirect(url_for('index'))  # Redirect to index page
    else:
        # Invalid credentials
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))  # Redirect back to login page

@app.route('/index')
@login_required
def index():
    return render_template('index.html', username=session['username'])

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        user = get_user(username)

        if user and user['password'] == old_password:
            return redirect(url_for('set_new_password', username=username))
        else:
            flash('Incorrect username or old password', 'error')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/login', methods=['POST'])
def authenticate():
    ...


@app.route('/set-new-password/<username>', methods=['GET', 'POST'])
def set_new_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            # Update the user's password in the database
            conn = sqlite3.connect('inspection.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
            conn.commit()
            conn.close()

            flash('Password updated successfully!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match', 'error')
            return redirect(url_for('set_new_password', username=username))

    return render_template('set_new_password.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
