from botocore.exceptions import ClientError
from app import app, ses_client
from flask import render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            response = ses_client.send_email(**msg)
        except ClientError as e:
            print(f"Error sending email: {e}")
        else:
            print(f"Email sent! Message ID: {response['MessageId']}")

def send_email(subject, sender, recipients, text_body, html_body):
    msg = {
        'Destination': {
            'ToAddresses': recipients
        },
        'Message': {
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': html_body,
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': text_body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        'Source': sender
    }
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['NOREPLY_EMAIL'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))