import sys
from entities.client import Client
import colored
from colored import fg, bg, attr

from ui.ui import UI

client = Client()
username = input("%s%s ENTER THE NAME %s" % (fg('white'), attr('bold'), attr('reset')))


if client.is_exists(username):
    client.connect(username)
else:
    if len(sys.argv) > 1:
        if sys.argv[1] == 'owner':
            client.add_owner(username)
        elif sys.argv[1] == 'admin':
            print('admin')
            client.add_admin(username)
        else:
            exit()
    else:
        client.add_user(username)
    client.connect(username)

ui = UI(username)
ui.start()
