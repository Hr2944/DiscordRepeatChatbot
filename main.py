import os

from botclient import BotClient

if __name__ == '__main__':

    try:
        with open('bot.key', 'r') as token_file:
            CLIENT_TOKEN = token_file.read().strip()
    except FileNotFoundError:
        CLIENT_TOKEN = os.environ.get('CLIENT_TOKEN', None)
    bot = BotClient()
    bot.run(CLIENT_TOKEN)
