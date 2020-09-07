from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.database.db import db


class UserModel(db.Model):
    # Specifying database table used for UserModel
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # personal data
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True)

    # security
    password_hash = db.Column(db.String(100))
    security_question = db.Column(db.String(80))
    security_answer = db.Column(db.String(80))

    # registration
    registration_date = db.Column(db.DateTime)
    terms_and_conditions_checked = db.Column(db.Boolean)

    # admin
    is_admin = db.Column(db.Boolean)

    # email verification
    is_email_verified = db.Column(db.Boolean)
    email_verification_date = db.Column(db.DateTime)

    # other info
    current_status = db.Column(db.Integer)

    bio = db.Column(db.String(500))
    location = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    slack_username = db.Column(db.String(80))
    social_media_links = db.Column(db.String(500))
    skills = db.Column(db.String(500))
    interests = db.Column(db.String(200))
    resume_url = db.Column(db.String(200))
    photo_url = db.Column(db.String(200))

    need_mentoring = db.Column(db.Boolean)
    available_to_mentor = db.Column(db.Boolean)

    def __init__(self, name, username, password, email,
                 security_question, security_answer, terms_and_conditions_checked):

        ## required fields

        self.name = name
        self.username = username
        self.email = email
        self.terms_and_conditions_checked = terms_and_conditions_checked

        # saving hash instead of saving password in plain text
        self.set_password(password)
        self.security_question = security_question
        self.security_answer = security_answer

        # default values
        self.is_admin = True if self.is_empty() else False  # first user is admin
        self.is_email_verified = False
        self.registration_date = datetime.now()

        ## optional fields

        self.need_mentoring = False
        self.available_to_mentor = False



    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'security_question': self.security_question,
            'security_answer': self.security_answer,
            'terms_and_conditions_checked': self.terms_and_conditions_checked,
            'registration_date': self.registration_date,
            'is_admin': self.is_admin,
            'is_email_verified': self.is_email_verified,
            'email_verification_date': self.email_verification_date,
            'current_status': self.current_status,
            'bio': self.bio,
            'location': self.location,
            'occupation': self.occupation,
            'slack_username': self.slack_username,
            'social_media_links': self.social_media_links,
            'skills': self.skills,
            'interests': self.interests,
            'resume_url': self.resume_url,
            'photo_url': self.photo_url,
            'need_mentoring': self.need_mentoring,
            'available_to_mentor': self.available_to_mentor
        }

    def __repr__(self):
        return "User name id %s. Username is %s ." % (self.name, self.username)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls):
        return cls.query.first() is None

    def set_password(self, password_plain_text):
        self.password_hash = generate_password_hash(password_plain_text)

    # checks if password is the same, using its hash
    def check_password(self, password_plain_text):
        return check_password_hash(self.password_hash, password_plain_text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
