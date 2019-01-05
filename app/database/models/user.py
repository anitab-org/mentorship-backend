import time

from werkzeug.security import generate_password_hash, check_password_hash
from app.database.sqlalchemy_extension import DB


class UserModel(DB.Model):
    # Specifying database table used for UserModel
    # pylint: disable=duplicate-code,too-many-arguments
    # pylint: disable=too-many-instance-attributes

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = DB.Column(DB.Integer, primary_key=True)

    # personal data
    name = DB.Column(DB.String(30))
    username = DB.Column(DB.String(30), unique=True)
    email = DB.Column(DB.String(30), unique=True)

    # security
    password_hash = DB.Column(DB.String(100))

    # registration
    registration_date = DB.Column(DB.Float)
    terms_and_conditions_checked = DB.Column(DB.Boolean)

    # admin
    is_admin = DB.Column(DB.Boolean)

    # email verification
    is_email_verified = DB.Column(DB.Boolean)
    email_verification_date = DB.Column(DB.DateTime)

    # other info
    current_mentorship_role = DB.Column(DB.Integer)
    membership_status = DB.Column(DB.Integer)

    bio = DB.Column(DB.String(500))
    location = DB.Column(DB.String(80))
    occupation = DB.Column(DB.String(80))
    organization = DB.Column(DB.String(80))
    slack_username = DB.Column(DB.String(80))
    social_media_links = DB.Column(DB.String(500))
    skills = DB.Column(DB.String(500))
    interests = DB.Column(DB.String(200))
    resume_url = DB.Column(DB.String(200))
    photo_url = DB.Column(DB.String(200))

    need_mentoring = DB.Column(DB.Boolean)
    available_to_mentor = DB.Column(DB.Boolean)

    def __init__(self, name, username, password, email,
                 terms_and_conditions_checked):
        # required fields
        # pylint: disable=too-many-arguments

        self.name = name
        self.username = username
        self.email = email
        self.terms_and_conditions_checked = terms_and_conditions_checked

        # saving hash instead of saving password in plain text
        self.set_password(password)

        # default values
        self.is_admin = (
            bool(self.is_empty())
        )  # first user is admin
        self.is_email_verified = False
        self.registration_date = time.time()

        # optional fields

        self.need_mentoring = False
        self.available_to_mentor = False

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "terms_and_conditions_checked": self.terms_and_conditions_checked,
            "registration_date": self.registration_date,
            "is_admin": self.is_admin,
            "is_email_verified": self.is_email_verified,
            "email_verification_date": self.email_verification_date,
            "current_mentorship_role": self.current_mentorship_role,
            "membership_status": self.membership_status,
            "bio": self.bio,
            "location": self.location,
            "occupation": self.occupation,
            "organization": self.organization,
            "slack_username": self.slack_username,
            "social_media_links": self.social_media_links,
            "skills": self.skills,
            "interests": self.interests,
            "resume_url": self.resume_url,
            "photo_url": self.photo_url,
            "need_mentoring": self.need_mentoring,
            "available_to_mentor": self.available_to_mentor,
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
    def get_all_admins(cls, is_admin=True):
        return cls.query.filter_by(is_admin=is_admin).all()

    @classmethod
    def is_empty(cls):
        return cls.query.first() is None

    def set_password(self, password_plain_text):
        self.password_hash = generate_password_hash(password_plain_text)

    # checks if password is the same, using its hash
    def check_password(self, password_plain_text):
        return check_password_hash(self.password_hash, password_plain_text)

    def save_to_db(self):
        DB.session.add(self)
        DB.session.commit()

    def delete_from_db(self):
        DB.session.delete(self)
        DB.session.commit()
