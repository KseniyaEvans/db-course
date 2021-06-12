import json
from entities.storage import Storage
from termcolor import colored


class Journal:
    logging = None
    storage = None
    pubsub = None

    def __init__(self, logger=True):
        self.storage = Storage()
        self.pubsub = self.storage.connection.pubsub()
        self.logging = logger
        self.pubsub.subscribe('ActivitiesJournal')
        print(colored('Journal created\nIncome activities will be displayed below', 'green'))

    def start(self):
        while True:
            pubsub_message = self.pubsub.get_message()
            if pubsub_message and pubsub_message['type'] == 'message':
                message = json.loads(pubsub_message['data'])
                message_type = message['type']
                if message_type == 'spam':
                    self.add_spammer(message['sender'])
                    if self.logging:
                        print(colored("User {} tried to send spam to {}".format(message['sender'], message['receiver']), 'red'))
                if message_type == 'connected':
                    self.user_connected()
                    if self.logging:
                        print(colored('User {} is online now!'.format(message['user']), 'cyan'))
                if message_type == 'disconnected':
                    self.user_disconnected()
                    if self.logging:
                        print(colored('User {} is offline now!'.format(message['user']), 'grey'))

    def user_connected(self):
        return self.storage.increment_online_count()

    def user_disconnected(self):
        return self.storage.decrement_online_count()

    def add_spammer(self):
        self.storage.increment_spam_count()
