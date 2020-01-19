from enum import Enum, unique, auto


@unique
class Message(Enum):
    USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER = auto()
    USER_ASSIGN_NOT_ADMIN = auto()
    USER_NOT_FOUND = auto()
    USER_IS_ALREADY_AN_ADMIN = auto()
    USER_IS_NOW_AN_ADMIN = auto()
    USER_DOES_NOT_EXIST = auto()
    USER_ADMIN_STATUS_WAS_REVOKED = auto()
    USER_IS_NOT_AN_ADMIN = auto()
    USER_CANNOT_REVOKE_ADMIN_STATUS = auto()
    USER_REVOKE_NOT_ADMIN = auto()

    def values(self):
        return list(map(str, self))
