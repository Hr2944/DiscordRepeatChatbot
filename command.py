import re

from singleton import singleton


class CommandSyntaxError(Exception):
    pass


class CommandNotRegisteredException(Exception):
    pass


class CommandActionException(Exception):
    pass


class ActionArguments:
    def __init__(self, command_name, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.command_name = command_name


class Action:
    def __init__(self, action, is_async=False):
        self.action = action
        self.is_async = is_async


@singleton
class CommandsRegistry:
    def __init__(self):
        self.commands: dict[str, Action] = {}

    def register(self, command, action, is_async=False):
        self.commands[command] = Action(action, is_async)

    def run(self, arguments: ActionArguments):
        command = self.get_command(arguments.command_name)
        if command:
            if command.is_async:
                raise CommandActionException(f'{command.action} is async, and should run via the "run_async" method')
            else:
                command.action(*arguments.args, **arguments.kwargs)

    async def run_async(self, arguments: ActionArguments):
        command = self.get_command(arguments.command_name)
        if command:
            if command.is_async:
                await command.action(*arguments.args, **arguments.kwargs)
            else:
                raise CommandActionException(f'{command.action} is not async, and should run via the "run" method')

    def get_command(self, command):
        return self.commands.get(command)

    def get_action(self, command):
        command = self.get_command(command)
        if command:
            return command.action
        return None

    def is_async(self, command):
        return self.get_command(command).is_async


class CommandParser:
    def __init__(self, message, prefix="!", suffix=" "):
        self.commands_registry = CommandsRegistry()
        # Don't use '$' char, as it cause bugs in regex
        self.command_prefix = prefix
        self.command_suffix = suffix
        self.parameterized_command_syntax = re.compile(rf'(?<={self.command_prefix})(.*?)(?={self.command_suffix})')
        self.not_parameterized_command_syntax = re.compile(rf'(?<={self.command_prefix})(.*)')
        self.message = self.clean_message(message)

    def parse(self):
        self.check_syntax()
        if self.is_parameterized():
            command = self.message.split(self.command_suffix)[0].split(self.command_prefix)[1]
            argument = self.message.split(self.command_suffix)[1]
        else:
            command = self.message.split(self.command_prefix)[1]
            argument = None
        if self.commands_registry.get_action(command) is None:
            raise CommandNotRegisteredException(f"Unknown command: {command}")
        return command, argument

    def clean_message(self, command):
        cleaned_command = command.strip().lower()
        if not cleaned_command.startswith(self.command_prefix):
            raise CommandSyntaxError(f"Command must start with {self.command_prefix}")
        return cleaned_command

    def is_parameterized(self):
        return self.parameterized_command_syntax.findall(self.message) != []

    def check_syntax(self):
        parameterized_matches = self.parameterized_command_syntax.findall(self.message)
        not_parameterized_matches = self.not_parameterized_command_syntax.findall(self.message)
        if len(parameterized_matches) != 1 and len(not_parameterized_matches) != 1:
            raise CommandSyntaxError(f"Incorrect command syntax: {self.message}")
