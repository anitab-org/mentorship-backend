from itsdangerous import URLSafeTimedSerializer, BadSignature

from flask_mail import Message
from flask import render_template

from app.api.mail_extension import mail

EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE = 86400  # 24 hours in seconds


def generate_confirmation_token(email):
    from run import application
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    return serializer.dumps(email, salt=application.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE):
    from run import application
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=application.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except BadSignature:
        return False
    return email


def send_email(recipient, subject, template):
    from run import application
    msg = Message(
        subject,
        recipients=[recipient],
        html=template,
        sender=application.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def send_email_verification_message(user_name, email):
    confirmation_token = generate_confirmation_token(email)
    from app.api.resources.user import UserEmailConfirmation  # import here to avoid circular imports
    from app.api import api
    confirm_url = api.url_for(UserEmailConfirmation, token=confirmation_token, _external=True)
    html = render_template('email_confirmation.html', confirm_url=confirm_url, user_name=user_name)
    subject = "Mentorship System - Please confirm your email"
    send_email(email, subject, html)
