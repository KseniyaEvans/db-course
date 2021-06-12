import redis
import time
import hashlib
from entities.constants import Status
from entities.constants import Role
from entities.constants import Tag
from Connection.redis_client import RedisClient
from Connection.neo4j_client import Neo4j

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
            self.neo4j = Neo4j()
        except Exception as e:
            print(e)

    # set
    def add_user(self, username):
        self.neo4j.registration(username, Role.USER)
        return self.connection.set(get_user_key(username), Role.USER, nx=True)

    def add_admin(self, username):
        self.neo4j.registration(username, Role.ADMIN)
        return self.connection.set(get_user_key(username), Role.ADMIN, nx=True)

    def add_owner(self, username):
        self.neo4j.registration(username, Role.OWNER)
        return self.connection.set(get_user_key(username), Role.OWNER, nx=True)

    def turn_into_admin(self, username):
        return self.connection.set(get_user_key(username), Role.ADMIN, nx=False)

    def turn_into_common_user(self, username):
        return self.connection.set(get_user_key(username), Role.USER, nx=False)

    def get_user(self, username):
        return self.connection.get(get_user_key(username))

    def add_message(self, message):
        hash_creator.update(str(time.time()).encode('utf-8'))
        message_object = {
            "Message": message.content, 
            "Status": Status.CREATED, 
            "Sender": message.sender,
            "Receiver": message.receiver}
        hashcode = hash_creator.hexdigest()[:10]
        self.connection.hmset(hashcode, message_object)
        self.push_message_hashcode_to_queue(hashcode)
        print(hashcode)
        self.neo4j.create_message(message.sender, message.receiver, message.tags, hashcode)
        
        return self.connection.lpush(get_message_key(message.sender), hashcode)

    # hash
    def update_message_status(self, hashcode, message_status):
        if message_status == Status.SPAM:
            self.neo4j.mark_message_as_spam(hashcode)
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
        self.neo4j.deliver_message(hashcode)
        return self.connection.lpush(get_inbox_key(receiver), hashcode)

    def get_messages_from_receiver(self, receiver, n_elem):
        return self.connection.lrange(get_inbox_key(receiver), 0, n_elem)

    def get_messages_from_sender(self, sender, n_elem):
        return self.connection.lrange(get_message_key(sender), 0, n_elem)

    # sorted set
    def increment_spam_count(self, username):
        return self.connection.zincrby(spam_key_string, 1, username)

    def get_spam(self, n_elem):
        return self.connection.zrange(spam_key_string, 0, n_elem, withscores=True, desc=True)

    def log_in(self, username):
        return self.neo4j.sign_in(username)

    def log_out(self, username):
        return self.neo4j.sign_out(username)

    def increment_online_count(self):
        return self.connection.incr('online')

    def decrement_online_count(self):
        return self.connection.decr('online')

    def get_online_count(self):
        return self.connection.get('online')

    # neo4g
    def get_users_with_tagged_messages(self, tags):
        res = self.neo4j.get_users_with_tagged_messages(tags)
        return res

    def get_users_with_n_long_relations(self, N: int):
        res = self.neo4j.get_users_with_n_long_relations(N)
        return res

    def shortest_way_between_users(self, user1, user2):
        res = self.neo4j.shortest_way_between_users(user1, user2)
        return res

    def get_users_which_have_only_spam_conversation(self):
        res = self.neo4j.get_users_which_have_only_spam_conversation()
        return res
        
    def get_unrelated_users_with_tagged_messages(self, tags):
        res = self.neo4j.get_unrelated_users_with_tagged_messages(tags)
        return res
