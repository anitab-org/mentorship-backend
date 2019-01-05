from flask_restplus import reqparse

AUTH_HEADER_PARSER = reqparse.RequestParser()
AUTH_HEADER_PARSER.add_argument(
    "Authorization",
    required=True,
    help="Authentication access token. E.g.: Bearer <access_token>",
    location="headers",
)
