from os import environ

API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
FILE_CAPTION = environ.get('FILE_CAPTION', '<code>{file_name}</code>')
OWNER = (environ.get('OWNER', ''))
PRIVATE_BOT = (environ.get('PRIVATE_BOT', False))
UPDATES_CHANNEL = environ.get('UPDATES_CHANNEL', 'https://t.me/webverseupdates')
SUPPORT_GROUP = environ.get('SUPPORT_GROUP', 'https://t.me/webversegroup')
DEV_LINK = environ.get('DEV_LINK', 'https://t.me/bhaiyajixbot')

# customise as per your need
