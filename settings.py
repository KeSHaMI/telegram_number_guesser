import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise Exception('Bot token must be present in environment')
