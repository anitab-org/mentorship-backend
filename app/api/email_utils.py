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

def send_email_request_notification(receiver_id, sender_id, sender_role, end_date, notes):
    """Sends a mentorship request message to the specified user.

    This function retrieves usernames and email addresses of mentorship request
    sender and receiver. It also converts timestamp to human readable format.
    It renders the email_confirmation.html template and sends email.

    Args:
        receiver_id: ID of person receiving mentorship request
        sender_id: ID of person receiving mentorship request
        sender_role: the role which request sender wants (mentor/mentee)
        end_date: ending date of mentorship relation
        notes: notes explaining about the mentorship request
    """
    from app.database.models.user import UserModel
    from datetime import datetime
    # retrieve objects based on id
    receiver = UserModel.find_by_id(receiver_id)
    sender = UserModel.find_by_id(sender_id)
    # convert timestamp to datetime
    dateTime = datetime.fromtimestamp(end_date)
    html = render_template(
        'request_notification.html',
        receiver_name = receiver.username,
        sender_name = sender.username,
        sender_email = sender.email,
        sender_role = sender_role ,
        end_date = dateTime.strftime("%d %b %Y"), # convert to human readable form "%d %b %Y"
        notes = notes
        )
    subject = "Mentorship System - You have a mentorship request!"
    send_email(receiver.email, subject, html)