import datetime

import click
from flask import Blueprint
from sqlalchemy import text

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from cli.utils import colorify_status, get_user

blueprint = Blueprint("relation", __name__)

dao = MentorshipRelationDAO()


@blueprint.cli.command("show")
@click.option("-id", "--user-id", type=int)
@click.option("-u", "--username")
@click.option("-e", "--email")
def show(user_id, username, email):
    """Shows data of a specified relation or lists all relations."""

    if not user_id:
        sql = text('SELECT * FROM mentorship_relations')
        result = db.engine.execute(sql)

        for row in result:
            print(dict(row))

    else:
        user = get_user(user_id, username, email)

        if not user:
            click.echo(click.style("User does not exist!", fg="red"))

        relations, status_code = dao.list_mentorship_relations(user_id)

        if not isinstance(relations, list):
            click.echo(click.style(relations["message"], fg="red"))
            return

        if not relations:
            click.echo(click.style("This user has no relationships", fg="red"))
            return

        for relation in relations:
            click.echo(click.style(str(relation)))


@blueprint.cli.command("send")
@click.option("-t", "--teach", is_flag=True)
@click.argument("sender_id")
@click.argument("recipient_id")
@click.option("-n", "--notes", default=None)
@click.option('--end_date', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(datetime.date.today() + datetime.timedelta(weeks=6)))
def send(teach, sender_id, recipient_id, notes, end_date):
    """
    Creates a mentorship relation between sender and recipient. By default sender is a mentee, and
    recipient is a mentor.

    :param teach: Boolean flag. If passed, sender is a mentor and recipient is a mentee (sender wants to teach recipient).
    :param sender_id: id of user who sends relationship request.
    :param recipient_id: id of user who receives relationship request.
    :param notes: Optional notes
    :param end_date: Date when relationship ends, e.g 2019-04-29
    """

    mentee_id = sender_id
    mentor_id = recipient_id

    if teach:
        mentee_id = recipient_id
        mentor_id = sender_id

    data = dict(
        mentor_id=mentor_id,
        mentee_id=mentee_id,
        end_date=end_date.timestamp(),
        notes=notes,
        tasks_list=TasksListModel()
    )

    message, status_code = dao.create_mentorship_relation(sender_id, data)
    color = colorify_status(status_code)

    click.echo(click.style(message["message"], fg=color))


@blueprint.cli.command("accept")
@click.argument("user_id", type=int)
@click.argument("request_id", type=int)
def accept(user_id, request_id):
    """Accepts a mentorship relation request"""

    message, status_code = dao.accept_request(user_id, request_id)
    color = colorify_status(status_code)

    click.echo(click.style(message["message"], fg=color))


@blueprint.cli.command("cancel")
@click.argument("user_id", type=int)
@click.argument("relation_id", type=int)
def cancel(user_id, relation_id):
    """Cancels a mentorship relation of a specific user"""

    message, status_code = dao.cancel_relation(user_id, relation_id)
    color = colorify_status(status_code)

    click.echo(click.style(message["message"], fg=color))
