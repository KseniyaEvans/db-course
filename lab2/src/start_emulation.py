# make sure start_journal.py, start_ui.py and start_worker.py are running

from time import sleep
from entities.client import Client
from ui import ui as Ui
import random
import string
from termcolor import colored


class Emulation:
    users_count = 0
    messages_count = 0
    message_lenght = 0
    users=[]
    

    def __init__(self):
        self.users_count = 10
        self.messages_count = 5
        self.message_lenght = 20
        self.client = Client()

    def create_users(self):
        for i in range(self.users_count):
            username = 'user' + str(i)
            if not self.client.is_exists(username):
                self.client.add_user(username)
                print(colored('{} added to Storage'.format(username), 'green'))
            else:
                print(colored('{} existed in Storage'.format(username), 'yellow'))
            self.users.append(username)

    def connect_user(self, username):
        if self.client.connect(username):
            for i in range(self.messages_count):
                self.send_messages(username)
            self.client.disconnect()
        else:
            print(colored('User {} does not exist'.format(username), 'red'))

    def get_random_string(self, lenght):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(lenght))
        
    def send_messages(self, sender):
        message = self.get_random_string(self.message_lenght)
        index = random.randint(0, len(self.users) - 1)
        while (self.users[index] == sender):
            index = random.randint(0, len(self.users) - 1)

        receiver = self.users[index]
        if self.client.is_exists(receiver):
            self.client.create_message(message, receiver)
            print('Message', colored(message[:8], 'cyan'), 'was sent to', colored(receiver, 'cyan'))
        else:
            print(colored('Unable send message to {}: user does not exist'.format(receiver), 'red'))

    def start(self):
        self.create_users()
        for username in self.users:
            self.connect_user(username)



emulation = Emulation()
emulation.start()

