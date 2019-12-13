from itsdangerous import URLSafeTimedSerializer, BadSignature

from flask_mail import Message
from flask import render_template

from app.api.mail_extension import mail

EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE = 86400  # 24 hours in seconds


def generate_confirmation_token(email):
    """Serializes and signs an email address into token with an expiry."""
    from run import application
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    return serializer.dumps(email, salt=application.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE):
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
    html = render_template('email_confirmation.html', confirm_url=confirm_url, user_name=user_name)
    subject = "Mentorship System - Please confirm your email"
    send_email(email, subject, html)


def send_email_new_request(user_sender, user_recipient, notes, sender_role):
    """Sends a notification html email message to the user_recipient user.

    First, the email address is serialized and signed for safety into a token.
    A confirmation url is generated using the token and a custom html email
    message containing the user's name and confirmation url is built and sent
    to the user.

    Args:
        user_sender: User who sent a relation request.
        user_recipient: User to which a relation request is addressed.
        note: Note from user_sender.
        sender_role: Role of the sender_user in the relationship. Must be either "mentee" or "mentor"
    """
    html = render_template('email_relation_request.html', user_recipient_name=user_recipient.name,
                           user_sender_name=user_sender.name, notes=notes, sender_role=sender_role)
    subject = "Mentorship System - You have got new relation request"
    send_email(user_recipient.email, subject, html)
