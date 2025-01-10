# email_notifications.py
from flask_mail import Mail, Message
from models import get_department_email

# Initialize Flask-Mail
mail = Mail()

def send_email(issue_category, issue_description):
    department_email = get_department_email(issue_category)  # Fetch email based on category
    subject = f'New {issue_category} Issue Reported'
    body = f'Issue Description: {issue_description}'
    
    msg = Message(subject, recipients=[department_email])
    msg.body = body
    mail.send(msg)
