import json

from entities.storage import Storage
from entities.constants import Message
from entities.constants import Role


class Client:
    storage_manager = Storage()
    username = None

    def connect(self, username):
        if self.is_exists(username):
            self.username = username
            self.storage_manager.connection.publish('ActivitiesJournal', json.dumps({'type': 'connected',
                                                                                     'user': username}))
            return True
        else:
            return False
    
    def add_user(self, username):
        self.storage_manager.add_user(username)

    def add_admin(self, username):
        self.storage_manager.add_admin(username)

    def add_owner(self, username):
        self.storage_manager.add_owner(username)

    def is_exists(self, username):
        return self.storage_manager.get_user(username) is not None

    def is_admin(self, username):
        return self.storage_manager.get_user(username) == Role.ADMIN

    def is_owner(self, username):
        return self.storage_manager.get_user(username) == Role.OWNER

    def is_common_user(self, username):
        return self.storage_manager.get_user(username) == Role.USER

    def promote_to_admin(self, username):
        self.storage_manager.turn_into_admin(username)

    def demote_to_user(self, username):
        self.storage_manager.turn_into_common_user(username)

    def create_message(self, content, receiver, tags):
        message = Message()
        message.content = content
        message.receiver = receiver
        message.sender = self.username
        message.tags = tags
        self.storage_manager.add_message(message)

    def get_message(self, hashcode):
        return self.storage_manager.get_message(hashcode)

    def get_inbox(self, username, n_elem):
        return self.storage_manager.get_messages_from_receiver(username, n_elem)

    def get_sent_messages(self, username, n_elem):
        return self.storage_manager.get_messages_from_sender(username, n_elem)

    def get_spammers(self, number_of_spammers):
        return self.storage_manager.get_spam(number_of_spammers)

    def log_in(self):
        return self.storage_manager.log_in(self.username)

    def log_out(self):
        return self.storage_manager.log_out(self.username)

    def get_online(self):
        return self.storage_manager.get_online_count()

    def disconnect(self):
        self.storage_manager.connection.publish('ActivitiesJournal', json.dumps({'type': 'disconnected',
                                                                                 'user': self.username}))

    def get_users_with_tagged_messages(self, tags):
        res = self.storage_manager.get_users_with_tagged_messages(tags)
        return res

    def get_users_with_n_long_relations(self, N: int):
        res = self.storage_manager.get_users_with_n_long_relations(N)
        return res

    def shortest_way_between_users(self, user1, user2):
        res = self.storage_manager.shortest_way_between_users(user1, user2)
        return res

    def get_users_which_have_only_spam_conversation(self):
        res = self.storage_manager.get_users_which_have_only_spam_conversation()
        return res
        
    def get_unrelated_users_with_tagged_messages(self, tags):
        res = self.storage_manager.get_unrelated_users_with_tagged_messages(tags)
        return res
        