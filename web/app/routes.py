from flask import render_template, flash, redirect, url_for, request
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('home.html', title='index')
    # return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, bio=form.bio.data, location=form.location.data, occupation=form.occupation.data, organization=form.organization.data, slack_username=form.slack_username.data, social_media_links=form.social_media_links.data, skills=form.skills.data, interests=form.interests.data, resume_url=form.resume_url.data, photo_url=form.photo_url.data, need_mentoring=form.need_mentoring.data, available_to_mentor=form.available_to_mentor.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Email or Password", 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))