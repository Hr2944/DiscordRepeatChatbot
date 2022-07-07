import discord

from question import QuestionSanitizer
from repeat import ChatBot
from session import ConversationSessions


class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author != self.user:
            question_sanitizer = QuestionSanitizer(message.content)
            if question_sanitizer.is_sanitize_safe():
                await message.channel.send(
                    self.get_answer_for_question(
                        question=question_sanitizer.sanitize(),
                        username=f"{message.author.name}#{message.author.discriminator}"
                    )
                )
            else:
                await message.channel.send(
                    f"Please ask a question by starting your sentence with '{question_sanitizer.question_prefix}'"
                )

    @staticmethod
    def get_answer_for_question(question, username):
        conversations = ConversationSessions()
        conversations.add_session_message(
            username=username,
            user_message=question
        )
        chatbot = ChatBot(question=question, for_username=username)
        answer = chatbot.respond()
        conversations.add_session_message(
            username=username,
            bot_message=answer
        )
        return answer
