import os

# You should set to the appropriate path!
MESSAGE_DIRECTORY = '/tmp/messages'


def get_new_message_id():
    """Get new message id"""
    existing_ids = os.listdir(MESSAGE_DIRECTORY)
    integer_ids = []
    for i in existing_ids:
        try:
            current_id = int(i)
            integer_ids.append(current_id)
        except:
            pass
    last_id = max(integer_ids)
    return last_id + 1


def save_message(sender, recipient, date, content):
    """Save the message"""
    message_id = get_new_message_id()
    with open(MESSAGE_DIRECTORY + '/' + str(message_id), 'w') as message_file:
        message_file.write(str(sender) + '\n')
        message_file.write(str(recipient) + '\n')
        message_file.write(str(date) + '\n')
        message_file.write(content + '\n')
    return message_id


def load_message(message_id):
    """Load the message"""
    with open(MESSAGE_DIRECTORY + '/' + str(message_id)) as message_file:
        sender = message_file.readline()
        recipient = message_file.readline()
        date = message_file.readline()
        content = message_file.readline()
        return {
            'sender': sender.rstrip('\n'),
            'recipient': recipient.rstrip('\n'),
            'date': date.rstrip('\n'),
            'content': content.rstrip('\n')
        }
