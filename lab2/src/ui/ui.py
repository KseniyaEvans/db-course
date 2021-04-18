from entities.client import Client
# from PyInquirer import prompt
from entities.constants import Role
from termcolor import colored

from consolemenu import SelectionMenu

common_ui = ['SEND MESSAGE', 'INBOX', 'SENT']
admin_ui = ['SEND MESSAGE', 'INBOX','SENT','GET ONLINE USERS', 'GET SPAMMERS RARING']
owner_ui = ['SEND MESSAGE', 'INBOX', 'GET ONLINE USERS', 'GET SPAMMERS RARING',
            'PROMOTE TO ADMIN', 'DEMOTE TO USUAL USER',]


class UI:
    client = Client()
    menu_type = None

    def __init__(self, client_name):
        self.client.username = client_name
        if self.client.is_admin(client_name):
            self.menu_type = Role.ADMIN
        elif self.client.is_owner(client_name):
            self.menu_type = Role.OWNER
        elif self.client.is_common_user(client_name):
            self.menu_type = Role.USER

    def start(self):
        while True:
            if (self.menu_type == Role.ADMIN):
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
            elif (self.menu_type == Role.USER):
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
            elif (self.menu_type == Role.OWNER):
                selectionMenu = SelectionMenu(
                owner_ui,
                title='Select the action:')
                selectionMenu.show()

                index = selectionMenu.selected_option
                if index == 0:
                    self.send_message()
                elif index == 1:
                    self.inbox()
                elif index == 2:
                    self.get_online_users()
                elif index == 3:
                    self.get_spammers_rating()
                elif index == 4:
                    self.promote_to_admin();
                elif index == 5:
                    self.demote_to_usual_user()
                else:
                    self.exit()       
            else:
                print('Bye, have a nice day!')
            
            
    def send_message(self):
        message = input('Message: ')
        receiver = input('Receiver: ')
        if self.client.is_exists(receiver):
            self.client.create_message(message, receiver)
        else:
            print(colored('Unable send message to {}: user does not exist'.format(receiver), 'red'))

    def inbox(self):
        messages = self.client.get_inbox(self.client.username, 10)
        if messages:
            message_list = []
            
            for hashcode in messages:
                mess = self.client.get_message(hashcode)
                new_str = colored(mess['Sender'], 'green') + '\t' + colored(mess['Status'], 'yellow') + '\t' + mess['Message']+ '\t'
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
            messages_sorted = sorted(messages, key=lambda message: message[1], reverse=True)
            print('Count: ', len(messages))
            print('Sent messages sorted by', colored('Status', 'yellow'))
            print('Sender\t\tReceiver\t\tStatus\t\t\tMessage')
            for hashcode in messages_sorted:
                mess = self.client.get_message(hashcode)
                print(colored(mess['Sender'], 'green') + '\t\t'+ mess['Receiver'] + '\t\t\t' + colored(mess['Status'], 'yellow') + '\t\t\t' + mess['Message']+ '\t')
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

    def promote_to_admin(self):
        username = input('Name: ')
        if self.client.is_admin(username) or self.client.is_owner(username):
            print(colored("User {} is already admin".format(username), 'red'))
        else:
            self.client.promote_to_admin(username)
        
    def demote_to_usual_user(self):
        username = input('Name: ')
        if self.client.is_common_user(username):
            print(colored("User {} is already common user".format(username), 'red'))
        else:
            self.client.demote_to_user(username)
        
    def exit(self):
        self.client.disconnect()
        quit()
