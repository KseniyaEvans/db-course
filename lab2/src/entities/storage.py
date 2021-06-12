import redis
import time
import hashlib
from entities.constants import Status
from entities.constants import Role
from Redis.redis_client import RedisClient


# key strings
user_key_string = "user"
spam_key_string = 'spam'
queue_key_string = 'queue'
message_key_string = "message"
inbox_key_string = 'inbox'


def get_user_key(username):
    return user_key_string + ':' + username


def get_spam_key(spammer_name):
    return spam_key_string + ':' + spammer_name


def get_message_key(message_sender_name):
    return message_key_string + ':' + message_sender_name


def get_inbox_key(receiver_name):
    return inbox_key_string + ':' + receiver_name


hash_creator = hashlib.sha512()


class Storage:
    connection = None
    def __init__(self):
        try:
            self.connection = RedisClient.get_connection()
        except Exception as e:
            print(e)

    # set
    def add_user(self, username):
        return self.connection.set(get_user_key(username), Role.USER, nx=True)

    def add_admin(self, username):
        return self.connection.set(get_user_key(username), Role.ADMIN, nx=True)

    def add_owner(self, username):
        return self.connection.set(get_user_key(username), Role.OWNER, nx=True)

    def turn_into_admin(self, username):
        return self.connection.set(get_user_key(username), Role.ADMIN, nx=False)

    def turn_into_common_user(self, username):
        return self.connection.set(get_user_key(username), Role.USER, nx=False)

    def get_user(self, username):
        return self.connection.get(get_user_key(username))

    def is_admin(self, username):
        return self.connection

    def add_message(self, message):
        hash_creator.update(str(time.time()).encode('utf-8'))
        message_object = {"Message": message.content, "Status": Status.CREATED, "Sender": message.sender,
                          "Receiver": message.receiver}
        hashcode = hash_creator.hexdigest()[:5]
        self.connection.hmset(hashcode, message_object)
        self.push_message_hashcode_to_queue(hashcode)
        return self.connection.lpush(get_message_key(message.sender), hashcode)

    # hash
    def update_message_status(self, hashcode, message_status):
        return self.connection.hset(hashcode, "Status", message_status)

    def get_message(self, hashcode):
        return self.connection.hgetall(hashcode)

    def get_message_receiver(self, hashcode):
        return self.connection.hget(hashcode, "Receiver")

    # list
    def push_message_hashcode_to_queue(self, hashcode):
        return self.connection.rpush(queue_key_string, hashcode)

    def get_message_hashcode_from_queue(self):
        return self.connection.lpop(queue_key_string)

    def send_message(self, hashcode, receiver):
        return self.connection.lpush(get_inbox_key(receiver), hashcode)

    def get_messages(self, receiver, n_elem):
        return self.connection.lrange(get_inbox_key(receiver), 0, n_elem)

    def get_messages_from_sender(self, sender, n_elem):
        return self.connection.lrange(get_message_key(sender), 0, n_elem)

    # sorted set
    def increment_spam_count(self, username):
        return self.connection.zincrby(spam_key_string, 1, username)

    def get_spam(self, n_elem):
        return self.connection.zrange(spam_key_string, 0, n_elem, withscores=True, desc=True)

    def increment_online_count(self):
        return self.connection.incr('online')

    def decrement_online_count(self):
        return self.connection.decr('online')

    def get_online_count(self):
        return self.connection.get('online')
