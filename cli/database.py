from datetime import datetime

import click
from flask import Blueprint

from app.api.dao.user import UserDAO
from app.database.sqlalchemy_extension import db
from cli.initial_data import data_admin, data_user_1, data_user_2
from cli.utils import print_user

blueprint = Blueprint("db", __name__)

userDAO = UserDAO()


@blueprint.cli.command("create")
def create_all():
    """ Creates all tables """
    db.create_all()
    click.echo(click.style("Created all tables", fg="green"))


@blueprint.cli.command("drop")
def drop_all():
    """ Drops (removes) all tables """
    if click.confirm('All tables will be dropped. Do you want to continue?'):
        db.drop_all()
        click.echo(click.style("Dropped all tables", fg="yellow"))
    else:
        print("Okay, operation aborted.")


@blueprint.cli.command("init")
def init():
    """Drops all tables and then creates fresh new. Then populates database with some initial data"""

    if click.confirm('All tables will be dropped. Do you want to continue?'):
        db.drop_all()
        db.create_all()
        populate()
        click.echo(click.style("Database was populated with initial data", fg="green"))
    else:
        print("Okay, operation aborted.")


def populate():
    """Populates database with some initial data."""

    # Registering a few dummy users
    register_new_user(data_admin)
    register_new_user(data_user_1)
    register_new_user(data_user_2)


def register_new_user(data):

    userDAO.create_user(data)

    # Confirm email registration
    user = userDAO.get_user_by_username(data["username"])

    user.is_email_verified = True
    user.email_verification_date = datetime.now()
    user.save_to_db()

    print_user(user)
