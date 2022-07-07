import discord

from question import QuestionSanitizer
from repeat import RepeatAndMemoizeBot
from session import ConversationSessions


class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if self.is_bot_channel(message):
            if self.should_reset(message):
                self.reset()
                await message.channel.send("Done.")
            else:
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

    def is_bot_channel(self, message):
        return message.author != self.user and "bot" in message.channel.name

    @staticmethod
    def get_answer_for_question(question, username):
        conversations = ConversationSessions()
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
        return answer

    @staticmethod
    def should_reset(message):
        return message.content == "$reset"

    @staticmethod
    def reset():
        sessions = ConversationSessions()
        sessions.reset()
