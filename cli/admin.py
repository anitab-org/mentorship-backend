import click
from flask import Blueprint

from app.api.dao.admin import AdminDAO
from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from cli.utils import print_user

adminDAO = AdminDAO()
userDAO = UserDAO()

blueprint = Blueprint("admin", __name__)


@blueprint.cli.command("show")
@click.option("-s", "--short", is_flag=True)
def show(short):
    """Lists all users with admin priviliges"""

    admins = UserModel.get_all_admins()
    for admin in admins:
        print_user(admin, short)


@blueprint.cli.command("assign")
@click.argument("username")
def assign(username):
    """Gives admin priviliges to user"""

    user = userDAO.get_user_by_username(username)

    if user:
        user.is_admin = True
        db.session.add(user)
        db.session.commit()

        click.echo(click.style(f"User {username} is now an Admin", fg="green"))
    else:
        click.echo(click.style(f"User {username} does not exist!", fg="red"))


@blueprint.cli.command("remove")
@click.argument("username")
def remove(username):
    """Revokes admin priviliges from user"""

    user = userDAO.get_user_by_username(username)

    if user:
        user.is_admin = False
        db.session.add(user)
        db.session.commit()

        click.echo(click.style(f"User {username} is no longer an Admin"))
    else:
        click.echo(click.style(f"User {username} does not exist!", fg="red"))
