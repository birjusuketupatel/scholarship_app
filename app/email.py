from app import app, mail
from flask_mail import Message

#wrapper function to send emails
def send_email(to, subject, template):
    msg = Message(subject,
                  recipients=[to],
                  html=template)
    mail.send(msg)
