from flask_restplus import reqparse

auth_header_parser = reqparse.RequestParser()
auth_header_parser.add_argument(
    "Authorization",
    required=True,
    help="Authentication access token. E.g.: Bearer <access_token>",
    location="headers",
)
