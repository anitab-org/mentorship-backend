from app import messages
from app.utils.validation_utils import validate_length, get_stripped_string

COMMENT_MAX_LENGTH = 400


def validate_task_comment_request_data(data):
    if "comment" not in data:
        return messages.COMMENT_FIELD_IS_MISSING

    comment = data["comment"]

    if not isinstance(comment, str):
        return messages.COMMENT_NOT_IN_STRING_FORMAT

    is_valid = validate_length(
        len(get_stripped_string(data["comment"])), 0, COMMENT_MAX_LENGTH, "comment"
    )
    if not is_valid[0]:
        return is_valid[1]

    return {}
