from flask_restplus import Api

api = Api(
    title="Mentorship System API",
    version="1.0",
    description="API documentation for the backend of Mentorship System. \n \n"
    + "Mentorship System is an application that matches women in tech to mentor each other, on career development, "
    + "through 1:1 relations during a certain period of time. \n \n"
    + "The main repository of the Backend System can be found here: https://github.com/anitab-org/mentorship-backend \n \n"
    + "The Android client for the Mentorship System can be found here: https://github.com/anitab-org/mentorship-android \n \n"
    + "For more information about the project here's a link to our wiki guide: https://github.com/anitab-org/mentorship-backend/wiki"
    # doc='/docs/'
)
api.namespaces.clear()

# Adding namespaces
from app.api.resources.user import users_ns as user_namespace

api.add_namespace(user_namespace, path="/")

from app.api.resources.admin import admin_ns as admin_namespace

api.add_namespace(admin_namespace, path="/")

from app.api.resources.mentorship_relation import (
    mentorship_relation_ns as mentorship_namespace,
)

api.add_namespace(mentorship_namespace, path="/")
