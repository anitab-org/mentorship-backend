from flask_restx import reqparse

auth_header_parser = reqparse.RequestParser()
auth_header_parser.add_argument(
    "Authorization",
    required=True,
    help="Authentication access token. E.g.: Bearer <access_token>",
    location="headers",
)

refresh_auth_header_parser = reqparse.RequestParser()
refresh_auth_header_parser.add_argument(
    "Authorization",
    required=True,
    help="Authentication refresh token. E.g.: Bearer <refresh_token>",
    location="headers",
)
