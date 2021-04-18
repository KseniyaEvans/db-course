class Message:
    content = ''
    status = ''
    sender = ''
    receiver = ''


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
