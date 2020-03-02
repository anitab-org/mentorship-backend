from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    bio = StringField('Bio')
    location = StringField('location')
    occupation = StringField('occupation')
    organization = StringField('organization')
    slack_username = StringField('slack_username')
    social_media_links = StringField('social_media_links')
    skills = StringField('skills')
    interests = StringField('interests')
    resume_url = StringField('resume_url')
    photo_url = StringField('photo_url')
    need_mentoring = BooleanField('need_mentoring')
    available_to_mentor = BooleanField('available_to_mentor')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')