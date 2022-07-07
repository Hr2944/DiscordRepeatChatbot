from bot import RepeatAndMemoizeBot
from session import ConversationSessionsRegistry


async def answer_question_command(question, message):
    username = f'{message.author.name}#{message.author.discriminator}'
    conversations = ConversationSessionsRegistry()
    conversations.add_session_message(
        username=username,
        user_message=question
    )
    chatbot = RepeatAndMemoizeBot(question=question, for_username=username)
    answer = chatbot.respond()
    conversations.add_session_message(
        username=username,
        bot_message=answer
    )
    await message.channel.send(answer)


async def reset_command(message):
    sessions = ConversationSessionsRegistry()
    sessions.reset()
    await message.channel.send("Reset done.")


async def help_command(message):
    await message.channel.send("""
    **Commands:**
    `!help` - show this message
    `!reset` - reset all the conversations
    `!question <question>` - ask the bot a question
    """)
