from bot import Bot

if __name__ == '__main__':
    with open('bot.key', 'r') as token_file:
        CLIENT_TOKEN = token_file.read().strip()
    bot = Bot()
    bot.run(CLIENT_TOKEN)
