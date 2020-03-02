from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    bio = db.Column(db.String(500))
    location = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    organization = db.Column(db.String(80))
    slack_username = db.Column(db.String(80))
    social_media_links = db.Column(db.String(500))
    skills = db.Column(db.String(500))
    interests = db.Column(db.String(200))
    resume_url = db.Column(db.String(200))
    photo_url = db.Column(db.String(200))

    need_mentoring = db.Column(db.Boolean)
    available_to_mentor = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))