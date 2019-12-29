from enum import Enum, unique, auto


@unique
class Message(Enum):
    USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER = auto()
    USER_ASSIGN_NOT_ADMIN = auto()
    USER_NOT_FOUND = auto()
    USER_IS_ALREADY_AN_ADMIN = auto()
    USER_IS_NOW_AN_ADMIN = auto()
    USER_DOES_NOT_EXIST = auto()

    def values(self):
        return list(map(str, self))
