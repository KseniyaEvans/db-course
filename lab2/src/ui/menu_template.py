# interfaces for promt
common_ui = [
    {
        'type': 'list',
        'message': 'Select operation',
        'name': 'operation',
        'choices': [
            {
                'name': 'SEND MESSAGE'
            },
            {
                'name': 'INBOX'
            },
            {
                'name': 'EXIT'
            }
        ]
    }
]

admin_ui = [
    {
        'type': 'list',
        'message': 'Select operation',
        'name': 'operation',
        'choices': [
            {
                'name': 'SEND MESSAGE'
            },
            {
                'name': 'INBOX'
            },
            {
                'name': 'GET ONLINE USERS'
            },
            {
                'name': 'GET SPAMMERS RARING'
            },
            {
                'name': 'EXIT'
            }
        ]
    }
]

owner_ui = [
    {
        'type': 'list',
        'message': 'Select operation',
        'name': 'operation',
        'choices': [
            {
                'name': 'SEND MESSAGE'
            },
            {
                'name': 'INBOX'
            },
            {
                'name': 'GET ONLINE USERS'
            },
            {
                'name': 'PROMOTE TO ADMIN'
            },
            {
                'name': 'DEMOTE TO USUAL USER'
            },
            {
                'name': 'GET SPAMMERS RARING'
            },
            {
                'name': 'EXIT'
            }
        ]
    }
]

input_name = [{
    'type': 'input',
    'name': 'value',
    'message': 'ENTER THE NAME'
}]

input_message = [{
    'type': 'input',
    'name': 'value',
    'message': 'ENTER THE MESSAGE'
}]

input_username = [{
    'type': 'input',
    'name': 'value',
    'message': 'ENTER THE USERNAME'
}]


def choose_message(messages):
    choice_message = [
        {
            'type': 'list',
            'name': 'value',
            'message': 'CHOOSE MESSAGE TO VIEW',
            'choices': []
        }
    ]
    for message in messages:
        obj = {
            'value': message['hashcode'],
            'name': message['message_str']
        }
        choice_message[0]['choices'].append(obj)
    return choice_message
