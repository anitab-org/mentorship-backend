from itsdangerous import URLSafeTimedSerializer, BadSignature

from flask_mail import Message
from flask import render_template

import config
from app.api.mail_extension import mail


def generate_confirmation_token(email):
    """Serializes and signs an email address into token with an expiry."""
    from run import application
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    return serializer.dumps(email, salt=application.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration= config.BaseConfig.UNVERIFIED_USER_THRESHOLD):
    """Confirms the token matches the expected email address.

    Args:
        token: Serialized and signed email address as a URL safe string.
        expiration: Maximum age of the token before expiration.

    Returns:
        email: Deserialized email address with verified signature.
        False: If the token signature does not match.

    Raises:
        SignatureExpired: Raised if the token's signature timestamp is older
            than the specified maximum age.
    """
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
    """Sends a html email message with a subject to the specified recipient."""
    from run import application
    msg = Message(
        subject,
        recipients=[recipient],
        html=template,
        sender=application.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def send_email_verification_message(user_name, email):
    """Sends a verification html email message to the specified user.

    First, the email address is serialized and signed for safety into a token.
    A confirmation url is generated using the token and a custom html email
    message containing the user's name and confirmation url is built and sent
    to the user.

    Args:
        user_name: User's name.
        email: User email address.
    """
    confirmation_token = generate_confirmation_token(email)
    from app.api.resources.user import UserEmailConfirmation  # import here to avoid circular imports
    from app.api.api_extension import api
    confirm_url = api.url_for(UserEmailConfirmation, token=confirmation_token, _external=True)
    html = render_template('email_confirmation.html', confirm_url=confirm_url, user_name=user_name,
                           threshold=config.BaseConfig.UNVERIFIED_USER_THRESHOLD)
    subject = "Mentorship System - Please confirm your email"
    send_email(email, subject, html)
