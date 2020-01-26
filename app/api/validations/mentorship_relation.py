from app import messages
from app.utils.enum_utils import MentorshipRelationState


def verify_request(request):
    # verify if request exists
    if request is None:
        return messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404

    # verify if request is in pending state
    if request.state != MentorshipRelationState.PENDING:
        return messages.NOT_PENDING_STATE_RELATION, 400

    return None
