import click as click
from flask import Blueprint

from app.api.dao.task import TaskDAO
from cli.utils import colorify_status

blueprint = Blueprint("task", __name__)

dao = TaskDAO()


@blueprint.cli.command("show")
@click.argument("user_id", type=int)
@click.argument("relation_id", type=int)
def show(user_id, relation_id):
    """Lists all tasks of the user """

    tasks = dao.list_tasks(user_id, relation_id)

    if not isinstance(tasks, list):
        click.echo(click.style(tasks[0]["message"], fg="red"))
        return

    if not tasks:
        click.echo(click.style("There are no tasks in this relation", fg="red"))
        return

    for relation in tasks:
        click.echo(click.style(str(relation)))


@blueprint.cli.command("create")
@click.argument("user_id", type=int)
@click.argument("relation_id", type=int)
@click.argument("description")
def create(user_id, relation_id, description):
    """Creates a new task"""

    data = {"description": description}

    message, status_code = dao.create_task(user_id, relation_id, data)

    color = colorify_status(status_code)
    click.echo(click.style(message["message"], fg=color))


@blueprint.cli.command("complete")
@click.argument("user_id", type=int)
@click.argument("relation_id", type=int)
@click.argument("task_id", type=int)
def complete(user_id, relation_id, task_id):
    """Marks specified task as completed"""

    message, status_code = dao.complete_task(user_id, relation_id, task_id)

    color = colorify_status(status_code)
    click.echo(click.style(message["message"], fg=color))


@blueprint.cli.command("delete")
@click.argument("user_id", type=int)
@click.argument("relation_id", type=int)
@click.argument("task_id", type=int)
def delete(user_id, relation_id, task_id):
    """Deletes specified task from a mentorship relation."""

    message, status_code = dao.delete_task(user_id, relation_id, task_id)

    color = colorify_status(status_code)
    click.echo(click.style(message["message"], fg=color))
