from enum import Enum

class Actions(Enum):
    NOT_SET=-1
    CHECK_FOR_REMINDER=1
    INSERT_TO_DB=2
    GET_ALL_REMINDERS=3
    DELETE_REMINDER=4
