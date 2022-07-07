import inspect

import discord

from actions import reset_command, answer_question_command, help_command
from command import CommandParser, CommandsRegistry, ActionArguments, CommandNotRegisteredException, CommandSyntaxError
from session import ConversationSessionsRegistry


class BotClient(discord.Client):
    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.sessions = ConversationSessionsRegistry()
        self.registry = CommandsRegistry()
        self.registry.register("reset", reset_command, True)
        self.registry.register("question", answer_question_command, True)
        self.registry.register("help", help_command, True)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if self.is_bot_channel(message):

            try:
                command_parser = CommandParser(message.content)
            except CommandSyntaxError:
                await message.channel.send(
                    f'Talk to me via the !question command, or use the !help command for more information.'
                )
                return

            try:
                command, argument = command_parser.parse()
            except CommandNotRegisteredException:
                await message.channel.send(
                    f'Unknown command: {message.content}\nType !help for more information.'
                )
                return
            except CommandSyntaxError:
                await message.channel.send(
                    f'Incorrect syntax for command: {message.content}\nType !help for more information.'
                )
                return

            action = self.registry.get_action(command)

            kwargs = {}
            if self.does_take_arg(action, "message"):
                kwargs["message"] = message

            run_arguments = ActionArguments(
                command_name=command,
                args=[argument] if argument else [],
                kwargs=kwargs
            )

            try:
                if self.registry.is_async(command):
                    await self.registry.run_async(run_arguments)
                else:
                    self.registry.run(run_arguments)
            except TypeError:
                await message.channel.send(
                    f'Incorrect parameters for command: !{command}\nType !help for more information.'
                )
                return

    def is_bot_channel(self, message):
        return message.author != self.user

    @staticmethod
    def does_take_arg(action, arg_name):
        spec = inspect.getfullargspec(action)
        return arg_name in spec.args or arg_name in spec.varargs or arg_name in spec.varkw or arg_name in spec.kwonlyargs
