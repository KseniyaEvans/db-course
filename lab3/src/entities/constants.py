from enum import Enum
class Message:
    content = ''
    status = ''
    sender = ''
    receiver = ''
    tags = []


class Status:
    CREATED = "CREATED"
    CHECK = "CHECK"
    QUEUE = "IN QUEUE"
    SPAM = "SPAM"
    SENT = "SENT"
    RECEIVED = "RECEIVED"


class Role:
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "COMMON USER"

class Tag(Enum):
    PERSONAL = 'PERSONAL'
    WORK = 'WORK'
    SOCIAL = 'SOCIAL'
    UPDATE = 'UPDATE'
    PROMOTION = 'PROMOTION'
    FORUM = 'FORUM'

    @classmethod
    def has_member(cls, value):
        return value in Tag._member_names_
