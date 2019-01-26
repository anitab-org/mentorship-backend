
class ResponseMessages:

    # Not found
    MENTOR_USER_DOES_NOT_EXIST = "Mentor user does not exist."
    MENTEE_USER_DOES_NOT_EXIST = "Mentee user does not exist."
    MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST = "This mentorship relation request does not exist."
    MENTORSHIP_RELATION_DOES_NOT_EXIST = "Mentorship relation does not exist."
    TASK_DOES_NOT_EXIST = "Task does not exist."
    USER_DOES_NOT_EXIST = "User does not exist."

    # Invalid fields
    NAME_INPUTTED_BY_USER_IS_INVALID = "Your name is invalid."
    EMAIL_INPUTTED_BY_USER_IS_INVALID = "Your email is invalid."
    USERNAME_INPUTTED_BY_USER_IS_INVALID = "Your username is invalid."
    TOKEN_IS_INVALID = "The token is invalid!"
    USER_ID_IS_NOT_VALID = "User id is not valid."
    TOKEN_IS_MISSING = "The authorization token is missing!"

    # Missing fields
    MENTOR_ID_FIELD_IS_MISSING = "Mentor ID field is missing."
    MENTEE_ID_FIELD_IS_MISSING = "Mentee ID field is missing."
    END_DATE_FIELD_IS_MISSING = "End date field is missing."
    NOTES_FIELD_IS_MISSING = "Notes field is missing."
    USERNAME_FIELD_IS_MISSING = "The field username is missing."
    PASSWORD_FIELD_IS_MISSING = "Password field is missing."
    NAME_NOT_IN_DATA = "Name field is missing."
    USERNAME_NOT_IN_DATA = "Username field is missing."
    EMAIL_FIELD_IS_MISSING = "Email field is missing."
    TERMS_AND_CONDITIONS_FIELD_IS_MISSING = "Terms and conditions field is missing."
    CURRENT_PASSWORD_FIELD_IS_MISSING = "Current password field is missing."
    NEW_PASSWORD_FIELD_IS_MISSING = "New password field is missing."
    AUTHORISATION_TOKEN_IS_MISSING = "The authorization token is missing!"

    # Admin
    USER_IS_ALREADY_AN_ADMIN = "User is already an Admin."
    USER_CANNOT_ASSIGN_HIMSELF_AS_ADMIN ="You cannot assign yourself as an Admin."
    USER_ADMIN_STATUS_WAS_REVOKED ="User admin status was revoked."
    USER_TRIES_TO_DELETE_HIS_ACCOUNT_WHILE_HE_IS_THE_ONLY_ADMIN_LEFT = "You cannot delete your account, since you are the only Admin left."
    USER_IS_NOT_AN_ADMIN = "User is not an Admin."
    USER_CANNOT_REVOKE_ADMIN_STATUS = "You cannot revoke your admin status."
    # MENTORSHIP_RELATION_DOES_NOT_EXIST = "This mentorship relation request does not exist."
    USER_TRIES_TO_ASSIGN_SOMEONE_ELSE_AS_ADMIN_WHEN_HE_HIMSELF_IS_NOT_AN_ADMIN = "You don't have admin status. You can't assign other user as admin."
    USER_TRIES_TO_REVOKE_SOMEONE_ELSE_AS_ADMIN_WHEN_HE_HIMSELF_IS_NOT_AN_ADMIN = "You don't have admin status. You can't revoke other admin user."
    USER_IS_NOW_AN_ADMIN = "User is now an Admin."

    # Mentor availability
    MENTOR_USER_IS_NOT_AVAILABLE_TO_MENTOR = "Mentor user is not available to mentor."
    MENTOR_USER_IS_ALREADY_IN_A_RELATIONSHIP = "Mentor user is already in a relationship."


    # Mentee availability
    MENTEE_USER_IS_NOT_AVAILABLE_TO_BE_MENTORED = "Mentee user is not available to be mentored."
    MENTEE_IS_ALREADY_IN_A_RELATIONSHIP = "Mentee user is already in a relationship."


    # Mismatch of fields
    USER_INPUTS_INCORRECT_MENTOR_ID_OR_MENTEE_ID = "Your ID has to match either Mentor or Mentee IDs."
    MENTEE_USER_IS_ALREADY_IN_A_RELATIONSHIP = "Mentee user is already in a relationship."

    # Relation constraints
    USER_INPUTS_MENTOR_ID_SAME_AS_MENTEE_ID = "You cannot have a mentorship relation with yourself."
    USER_INPUTS_END_TIME_BEFORE_PRESENT_TIME = "End date is invalid since date has passed."
    USER_INPUTS_MENTORSHIP_TIME_GREATER_THAN_MAXIMUM_TIME = "Mentorship relation maximum duration is 6 months."
    USER_INPUTS_MENTORSHIP_TIME_LESSER_THAN_MINIMUM_TIME = "Mentorship relation minimum duration is 4 week."
    USER_CANNOT_ACCEPT_A_MENTORSHIP_REQUEST_SENT_BY_HIMSELF="You cannot accept a mentorship request sent by yourself."
    USER_CANNOT_ACCEPT_A_MENTORSHIP_RELATION_WHERE_HE_IS_NOT_INVOLVED="You cannot accept a mentorship relation where you are not involved."
    USER_CANNOT_REJECT_A_RELATIONSHIP_REQUEST_SENT_BY_HIMSELF_FOR_A_MENTOR="You cannot reject a mentorship request sent by yourself."
    USER_CANNOT_REJECT_A_RELATIONSHIP_REQUEST_WHERE_HE_IS_NOT_INVOLVED="You cannot reject a mentorship relation where you are not involved."
    USER_CANNOT_CANCEL_A_RELATIONSHIP_REQUEST_WHERE_HE_IS_NOT_INVOLVED="You cannot cancel a mentorship relation where you are not involved."
    USER_CANNOT_DELETE_A_RELATIONSHIP_REQUEST_WHICH_HE_DID_NOT_CREATE="You cannot delete a mentorship request that you did not create."
    USER_IS_NOT_IN_A_MENTORED_RELATIONSHIP_CURRENTLY = "You are not in a current mentorship relation."
    USER_IS_NOT_INVOLVED_IN_THIS_MENTORSHIP_RELATION = "You are not involved in this mentorship relation."
    USER_USES_A_USERNAME_THAT_ALREADY_EXISTS = ["A user with that username already exists","That username is already taken by another user."]
    USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS = "A user with that email already exists"
    USER_IS_NOT_REGISTERED_IN_THE_SYSTEM = "You are not registered in the system."
    USER_USES_A_NAME_OF_LENGTH_GREATER_THAN_MAXIMUM_LIMIT = "The {field_name} field has to be shorter than {max_limit} characters."
    USER_USES_A_NAME_OF_LENGTH_LESSER_THAN_MINIMUM_LIMIT = "The {field_name} field has to be longer than {min_limit} characters and shorter than {max_limit} characters."
    USER_INPUTS_INCORRECT_CONFIGURATION_VALUE = "The environment config value has to be within these values: prod, dev, test."

    # Mentorship state
    MENTOR_RELATIONSHIP_IS_NOT_IN_PENDING_STATE = "This mentorship relation is not in the pending state."
    USER_RELATIONSHIP_STATUS_IS_NOT_IN_ACCEPTED_STATE = "This mentorship relation is not in the accepted state."
    MENTORSHIP_RELATION_IS_NOT_IN_ACCEPTED_STATE = "Mentorship relation is not in the accepted state."
    USER_CURRENTLY_INVOLVED_IN_MENTORSHIP_RELATION ="You are currently involved in a mentorship relation."
    MENTORSHIP_RELATION_WAS_REJECTED_SUCCESSFULLY = "Mentorship relation was rejected successfully."
    MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY = "Mentorship relation was cancelled successfully."


    # Login errors
    USER_ENTERS_INCORRECT_PASSWORD = "Current password is incorrect."
    EMAIL_FROM_TOKEN_HAS_EXPIRED_OR_IS_INVALID = "The confirmation link is invalid or the token has expired."
    USERNAME_OR_PASSWORD_FIELD_IS_INCORRECTLY_FILLED_UP = "Username or password is wrong."
    USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN = "Please verify your email before login."
    NAME_USERNAME_AND_PASSWORD_ARE_NOT_IN_STRING_FORMAT = "Name, username and password must be in string format."
    TERMS_AND_CONDITIONS_ARE_NOT_CHECKED = "Terms and conditions are not checked."
    USER_INPUTS_SPACE_IN_PASSWORD = "Password shouldn't contain spaces."
    TOKEN_HAS_EXPIRED = "The token has expired! Please, login again."
    TOKEN_SENT_TO_EMAIL_OF_USER = "Token sent to the user's email"
    EMAIL_VERIFICATION_MESSAGE = "Check your email, a new verification email was sent."

    # Success messages
    TASK_WAS_ALREADY_ACHIEVED = "Task was already achieved."
    MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY = "Mentorship relation was sent successfully."
    MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY = "Mentorship relation was accepted successfully."
    MENTORSHIP_RELATION_WAS_DELETED_SUCCESSFULLY = "Mentorship relation was deleted successfully."
    TASK_WAS_CREATED_SUCCESSFULLY = "Task was created successfully."
    TASK_WAS_DELETED_SUCCESSFULLY = "Task was deleted successfully."
    TASK_WAS_ALREADY_ACHIEVED_SUCCESSFULLY = "Task was achieved successfully."
    USER_WAS_CREATED_SUCCESSFULLY = "User was created successfully.A confirmation email has been sent via email.After confirming your email you can login."
    ACCEPT_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Accept mentorship relations with success."
    REJECTED_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Rejected mentorship relations with success."
    CANCELLED_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Cancelled mentorship relations with success."
    DELETED_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Deleted mentorship relations with success."
    RETURNED_PAST_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Returned past mentorship relations with success."
    RETURNED_CURRENT_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Returned current mentorship relation with success."
    RETURNED_PENDING_MENTORSHIP_RELATIONS_WITH_SUCCESS = "Returned pending mentorship relations with success."
    DELETE_TASK_WITH_SUCCESS = "Delete task with success."
    UPDATED_TASK_WITH_SUCCESS = "Updated task with success."
    USER_SUCCESSFULLY_CREATED = "User successfully created."

    # Miscellaneous
    NOT_IMPLEMENTED = "Not implemented."
    VALIDATION_ERROR = "Validation error."
    NOT_IMPLEMENTED = "Not implemented."