import click as click

from app.database.models.user import UserModel


def get_user(user_id, username, email):
    """Convenient method to get user by user_id, username or email."""
    user = None

    if user_id:
        user = UserModel.find_by_id(user_id)
    elif username:
        user = UserModel.find_by_username(username)
    elif email:
        user = UserModel.find_by_email(email)

    return user


def print_user(user, short=False):
    """Pretty-prints UserModel"""
    click.echo(
        click.style(f"id: {user.id}, username: {user.username}, email: {user.email}, name: {user.name}"))
    if not short:
        click.echo(user)


def colorify_status(status_code):
    """If status code is 200, returns green, else returns red."""
    return "green" if status_code == 200 else "red"
