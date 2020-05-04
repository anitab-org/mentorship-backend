from enum import IntEnum, unique


@unique
class MentorshipRelationState(IntEnum):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    CANCELLED = 4
    COMPLETED = 5

    def values(self) -> list:
        return list(map(int, self))
