from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(issue_category, transcription, email):
    try:
        # Set up the message
        msg = MIMEMultipart()
        msg['From'] = 'bapan.dgart@gmail.com'  # Replace with your email
        msg['To'] = email
        msg['Subject'] = f'Issue Categorized as {issue_category}'
        
        # Body of the email
        body = f"Issue: {issue_category}\nTranscription: {transcription}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Set up the server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('bapan.dgart@gmail.com', 'tcqq puzw kptj tfsm')  # Replace with your email credentials
            text = msg.as_string()
            server.sendmail('bapan.dgart@gmail.com', email, text)  # Replace with your email

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
