from flask_restx import Api

# Adding namespaces
from app.api.resources.user import users_ns as user_namespace
from app.api.resources.admin import admin_ns as admin_namespace
from app.api.resources.mentorship_relation import (
    mentorship_relation_ns as mentorship_namespace,
)
from app.api.resources.task import task_ns as task_namespace
from app.api.resources.task_comment import task_comment_ns as task_comment_namespace


def androidlink():
    return "<a href=https://github.com/anitab-org/mentorship-android>Android</a>"


def flutterlink():
    return "<a href=https://github.com/anitab-org/mentorship-flutter>Flutter</a>"


def ioslink():
    return "<a href=https://github.com/anitab-org/mentorship-ios>iOS</a>"


api = Api(
    title="Mentorship System API",
    version="1.0",
    description="API documentation for the backend of Mentorship System. \n \n"
    + "Mentorship System is an application that matches women in tech to mentor each other, on career "
    "development, through 1:1 relations during a certain period of time. \n \n"
    + "The main repository of the Backend System can be found here: "
    "https://github.com/anitab-org/mentorship-backend "
    + "\n\nThe clients for the Mentorship System: \n"
    + androidlink()
    + " | "
    + flutterlink()
    + " | "
    + ioslink()
    + "\n\nGet started to using Backend Swagger UI here: "
    "https://github.com/anitab-org/mentorship-backend/wiki/Using-Backend-Swagger-UI "
    + "\n\nFor more information about the project here's a link to our wiki guide: "
    "https://github.com/anitab-org/mentorship-backend/wiki "
    + "\n\nThis <a href=https://github.com/anitab-org/mentorship-backend/blob/develop/docs/quality"
    "-assurance-test-cases.md>Quality Assurance Test cases</a> document contains examples of test "
    "scenarios to evaluate if the API is working as it should.",
)
api.namespaces.clear()

api.add_namespace(user_namespace, path="/")

api.add_namespace(admin_namespace, path="/")

api.add_namespace(mentorship_namespace, path="/")

api.add_namespace(task_namespace, path="/")

api.add_namespace(task_comment_namespace, path="/")
