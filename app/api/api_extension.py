from flask_restplus import Api

from app.api.resources.mentorship_relation import (
    MENTORSHIP_RELATION_NS as mentorship_namespace,
)
from app.api.resources.admin import ADMIN_NS as admin_namespace
from app.api.resources.user import USERS_NS as user_namespace

API = Api(
    title="Mentorship System API",
    version="1.0",
    description="API documentation for the backend of Mentorship System"
    # doc='/docs/'
)

# Adding namespaces

API.add_namespace(user_namespace, path="/")


API.add_namespace(admin_namespace, path="/")


API.add_namespace(mentorship_namespace, path="/")
