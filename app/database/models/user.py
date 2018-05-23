from app.database.db import db
from datetime import datetime


class UserModel(db.Model):
    # Specifying database table used for UserModel
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # personal data
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True)

    # TODO security, save password as a hash

    # security
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

    def __init__(self, name, username, password, email,
                 security_question, security_answer, terms_and_conditions_checked):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.security_question = security_question
        self.security_answer = security_answer
        self.terms_and_conditions_checked = terms_and_conditions_checked

        # default values
        self.is_admin = True if self.is_empty() else False  # first user is admin
        self.is_email_verified = False
        self.registration_date = datetime.now()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'security_question': self.security_question,
            'security_answer': self.security_answer,
            'terms_and_conditions_checked': self.terms_and_conditions_checked,
            'registration_date': self.registration_date,
            'is_admin': self.is_admin,
            'is_email_verified': self.is_email_verified,
            'email_verification_date': self.email_verification_date
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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
