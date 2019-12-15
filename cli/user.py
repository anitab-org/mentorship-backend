from datetime import datetime

import click
from flask import Blueprint

from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from cli.utils import print_user, get_user

dao = UserDAO()

blueprint = Blueprint("user", __name__)


@blueprint.cli.command("show")
@click.option("-id", "--user-id", type=int)
@click.option("-u", "--username")
@click.option("-e", "--email")
@click.option("-s", "--short", is_flag=True)
def show(user_id, username, email, short):
    """Shows data of a specified user or lists all users."""

    user = get_user(user_id, username, email)

    if user:
        print_user(user, short)
    else:
        if not user_id and not user_id and not email:
            users_list = UserModel.query.all()

            for user in users_list:
                print_user(user, short)
        else:
            click.echo(click.style(f"User does not exist!", fg="red"))


@blueprint.cli.command("create")
@click.option("--name", prompt="Enter name")
@click.option("--username", prompt="Enter username")
@click.option("--email", prompt="Enter email")
@click.option("--password", prompt="Enter password", default="abcd1234")
@click.option("-no-veri", "--email-not-verified", is_flag=True)
def create(name, username, email, password, email_not_verified):
    """Creates a new user"""

    data = dict(
        name=name,
        username=username,
        email=email,
        password=password,
        terms_and_conditions_checked=True)

    message, status_code = dao.create_user(data)

    color = "green" if status_code == 200 else "red"

    click.echo(click.style(f"code {status_code}: {message['message']}", fg=color))

    if status_code == 200 and not email_not_verified:
        user = dao.get_user_by_username(username)
        user.is_email_verified = True
        user.email_verification_date = datetime.now()
        user.save_to_db()
        click.echo(click.style("User's email address was automatically confirmed!", fg="green"))


@blueprint.cli.command("update")
@click.option("-id", "--user-id", type=int)
@click.option("-u", "--username")
@click.option("-e", "--email")
@click.option("-n", "--name")
@click.option("-b", "--bio")
@click.option("-loc", "--location")
@click.option("-occ", "--occupation")
@click.option("-org", "--organization")
@click.option("-slack", "--slack-username")
@click.option("--social-media-links")
@click.option("--skills")
@click.option("--interests")
@click.option("--resume_url")
@click.option("--photo-url")
@click.option("-mentee", "--need-mentoring", type=bool)
@click.option("-mentor", "--available-to-mentor", type=bool)
def update(user_id, username, email, name, bio, location, occupation, organization, slack_username, social_media_links,
           skills,
           interests, resume_url, photo_url, need_mentoring, available_to_mentor):
    """Updates user with new data"""

    user = get_user(user_id, username, email)

    if not user:
        click.echo(click.style("User does not exist!", fg="red"))
        return

    data = dict()

    if name:
        data["name"] = name
    if bio:
        data["bio"] = bio
    if location:
        data["location"] = location
    if occupation:
        data["occupation"] = occupation
    if organization:
        data["organization"] = organization
    if slack_username:
        data["slack_username"] = slack_username
    if social_media_links:
        data["social_media_links"] = social_media_links
    if skills:
        data["skills"] = skills
    if interests:
        data["interests"] = interests
    if resume_url:
        data["resume_url"] = resume_url
    if photo_url:
        data["photo_url"] = photo_url
    if need_mentoring:
        data["need_mentoring"] = need_mentoring
    if available_to_mentor:
        data["available_to_mentor"] = available_to_mentor

    print(f"Update delta: {data}")

    message, status_code = dao.update_user_profile(user.id, data)

    color = "green" if status_code == 200 else "red"
    click.echo(click.style(message["message"], fg=color))


@blueprint.cli.command("delete")
@click.option("-id", "--user-id", type=int)
@click.option("-u", "--username")
@click.option("-e", "--email")
def delete(user_id, username, email):
    """Deletes a user"""
    if not user_id and not username and not email:
        click.echo(click.style("No parameters passed. Type 'flask user delete --help'", fg="red"))
    else:
        user = get_user(user_id, username, email)

        if user:
            user.delete_from_db()
            click.echo(click.style(f"User was successfully deleted", fg="yellow"))
        else:
            click.echo(click.style(f"User does not exist!", fg="red"))
