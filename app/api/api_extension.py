from flask_restplus import Api

api = Api(
    title="Mentorship System API",
    version="1.0",
    description="API documentation for the backend of Mentorship System"
    # doc='/docs/'
)

# Adding namespaces
from app.api.resources.user import users_ns as user_namespace

api.add_namespace(user_namespace, path="/")

from app.api.resources.admin import admin_ns as admin_namespace

api.add_namespace(admin_namespace, path="/")

from app.api.resources.mentorship_relation import (
    mentorship_relation_ns as mentorship_namespace,
)

api.add_namespace(mentorship_namespace, path="/")
