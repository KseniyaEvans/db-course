from redis import client
from entities.client import Client
from entities.constants import Role
from entities.constants import Status
from entities.constants import Tag
from termcolor import colored
import random
from consolemenu import SelectionMenu
from consolemenu import MultiSelectMenu

main_ua = ['User', 'Neo4j']
common_ui = ['SEND MESSAGE', 'INBOX', 'SENT']
admin_ui = ['SEND MESSAGE', 'INBOX','SENT','GET ONLINE USERS', 'GET SPAMMERS RARING']

neo4j_ui = [
    'Find users with tags',
    'Find users with N length of relations',
    'Find the shortest way between users',
    'Find users only with spam messages',
    'Find unrelated users with tags',
    ]


class UI:
    client = Client()
    menu_type = None

    def __init__(self, client_name):
        self.client.username = client_name
        if self.client.is_admin(client_name):
            self.menu_type = Role.ADMIN
        elif self.client.is_common_user(client_name):
            self.menu_type = Role.USER

    def start(self):
        self.client.log_in()
        while True:
            selectionMenu = SelectionMenu(
                main_ua,
                title='Select the mode:')
            selectionMenu.show()
            
            index = selectionMenu.selected_option
            if index == 0:
                if self.menu_type == Role.ADMIN:
                    self.admin_menu()           
                elif self.menu_type == Role.USER:
                    self.user_menu()
            elif index == 1:
                neo4jMenu = SelectionMenu(
                neo4j_ui,
                title='Select the action:')
                neo4jMenu.show()
                i= neo4jMenu.selected_option
                self.neo4j_menu(i)
            else:
                self.exit()  
            
    def neo4j_menu(self, index):
        if index == 0:
            for i in range(0, len(Tag._member_names_)):
                print('{}. {}'.format(i, Tag._member_names_[i]))
            index = input('Enter the index of tags:\n')
            index = index.replace(' ', ',').split(',')
            tags = [Tag._member_names_[int(i)] for i in index if i!='']
            print(index, tags)
            users = self.client.get_users_with_tagged_messages(tags)
            print(users)
            input()

        elif index == 1:
            N = int(input('Enter N:\n'))
            relations = self.client.get_users_with_n_long_relations(N)
            print(relations)

        elif index == 2:
            user1 = input('Enter first username: ')
            user2 = input('Enter second username: ')
            way = self.client.shortest_way_between_users(user1, user2)
            for i in range(0, len(way)):
                print(way[i], end='')
                if i != len(way)-1:
                    print(' -> ', end='')

        elif index == 3:
            spam_users = self.client.get_users_which_have_only_spam_conversation()
            for pair in spam_users:
                print(pair[0], ' -> ', pair[1])
                
        elif index == 4:
            for i in range(0, len(Tag._member_names_)):
                print('{}. {}'.format(i, Tag._member_names_[i]))
            index = input('Enter the index of tags:\n')
            index = index.replace(' ', ',').split(',')
            tags = [Tag._member_names_[int(i)] for i in index if i!='']
            print(index, tags)
            users = self.client.get_unrelated_users_with_tagged_messages(tags)
            print(users)
            input()
            
    def admin_menu(self):
        selectionMenu = SelectionMenu(
            admin_ui,
            title='Select the action:')
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index == 0:
            self.send_message()
        elif index == 1:
            self.inbox()
        elif index == 2:
            self.sent()
        elif index == 3:
            self.get_online_users()
        elif index == 4:
            self.get_spammers_rating()
        else:
            self.exit()

    def user_menu(self):
        selectionMenu = SelectionMenu(
            common_ui,
            title='Select the action:') 
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index == 0:
            self.send_message()
        elif index == 1:
            self.inbox()
        elif index == 2:
            self.sent()
        else:
            self.exit()   


    def generate_tags(self):
        length = random.randint(2, len(Tag._member_names_) - 1)
        index = []
        for i in range(1, length):
            id = random.randint(0, len(Tag._member_names_) - 1)
            if id not in index:
                index.append(id)

        tags = [Tag._member_names_[i] for i in index]
        return tags
          
    def send_message(self):
        message = input('Message: ')
        receiver = input('Receiver: ')
        tags = self.generate_tags()
        if self.client.is_exists(receiver):
            self.client.create_message(message, receiver, tags)
            print(
                'Message', colored(message[:8], 'cyan'), 
                'was sent to', colored(receiver, 'cyan'), 
                'with tags: ', colored(tags, 'cyan'))
        else:
            print(colored('Unable send message to {}: user does not exist'.format(receiver), 'red'))

    def inbox(self):
        messages = self.client.get_inbox(self.client.username, 10)
        if messages:
            message_list = []
            
            for hashcode in messages:
                mess = self.client.get_message(hashcode)
                status_col = 'yellow'
                if (mess['Status'] == "SPAM"):
                    status_col = 'red'
                elif (mess['Status'] == 'RECEIVED'):
                    status_col = 'green'
                elif (mess['Status'] == 'CREATED'):
                    status_col = 'cyan'
                
                new_str = colored(mess['Sender'], 'green') + '\t' + colored(mess['Status'], status_col) + '\t' + mess['Message']+ '\t'
                message_list.append(new_str)

            selectionMenu = SelectionMenu(
                message_list,
                title='Choose the message to view', 
                subtitle='Count: '+ str(len(messages)))
            selectionMenu.show()
            index = selectionMenu.selected_option

            if (index < len(messages)):
                hashcode_new = messages[index]
                mess = self.client.get_message(hashcode_new)
                input(colored(mess['Sender'], 'green') + '\t' + colored(mess['Status'], 'yellow') + '\t' + mess['Message']+ '\t')
                self.client.storage_manager.update_message_status(hashcode_new, 'RECEIVED')
        else:
            print(colored('No messages', 'yellow'))
            input()

    def sent(self):
        messages = self.client.get_sent_messages(self.client.username, 10)
        if messages:
            print('Count: ', len(messages))
            print('Sender\t\tReceiver\t\tStatus\t\t\tMessage')
            for hashcode in messages:
                mess = self.client.get_message(hashcode)

                status_col = 'yellow'
                if (mess['Status'] == "SPAM"):
                    status_col = 'red'
                elif (mess['Status'] == 'RECEIVED'):
                    status_col = 'green'
                elif (mess['Status'] == 'CREATED'):
                    status_col = 'cyan'

                print(colored(mess['Sender'], 'green') + '\t\t'+ mess['Receiver'] + '\t\t\t' + colored(mess['Status'], status_col) + '\t\t\t' + mess['Message']+ '\t')
        else:
            print(colored('No messages', 'yellow'))
        input()


    def get_spammers_rating(self):
        spammers = self.client.get_spammers(10)
        for spammer in spammers:
            print(colored(spammer[0] + ': {} '.format(int(spammer[1])) + 'spam messages', 'red'))
        input()

    def get_online_users(self):
        print(self.client.get_online())
        input()
        
    def exit(self):
        print('Bye, have a nice day!')
        self.client.disconnect()
        self.client.log_out()
        quit()
