from .librus_session import LibrusSession
from .command_parsing import parse_command
from .exceptions import ParsingException, TerminalAuthorizationException
import re

from . import messages_commands
from . import other_commands
from . import authorization_commands
from . import help_command


class LibrusTerminal():

    enable_color = True
    commands = {
        "gmes": messages_commands.get_messages_command,
        "exit": other_commands.exit_command,
        "cls": other_commands.clear_command,
        "clear": other_commands.clear_command,
        "login": authorization_commands.login_command,
        "logout": authorization_commands.logout_command,
        "rmes": messages_commands.read_message_command,
        "help": help_command.help_command
    }

    def __init__(self, session: LibrusSession) -> None:
        self.session: LibrusSession = session

    @property
    def _input_message(self) -> str:
        logged_in = True

        try:
            self.session.check_if_expired()

        except TerminalAuthorizationException as exception:
            logged_in = False

        attrs = ("logged in", "BLUE") if logged_in else ("not logged in", "RED")

        message =\
            self._color("[Librus (", "GREEN") +\
            self._color(*attrs) +\
            self._color(")] >> ", "GREEN")

        return message

    @classmethod
    def _color(cls, text, col):

        if not cls.enable_color:
            return text

        colors = {
            "BLUE": '\033[94m',
            "GREEN": '\033[92m',
            "YELLOW": '\033[93m',
            "RED": '\033[91m',
            "ENDC": '\033[0m',
        }

        col = colors.get(col, "")

        return col + text + (colors["ENDC"] if col else "")

    def run_terminal(self) -> None:
        while True:
            try:
                command = input(self._input_message)
            except KeyboardInterrupt:
                exit()

            if not command:
                continue

            try:
                options, arguments = parse_command(command)
            except ParsingException as exception:
                print(str(exception), *exception.errors)
                continue

            except ValueError as exception:
                print("niepoprawnie sformatowana komenda", str(exception))
                continue

            command, options = options[0], options[1:]

            if command not in self.commands:
                print("nie ma takiej komendy:", command)
                continue

            try:
                result = self.commands[command](self.session, *options, **arguments)

            except TerminalAuthorizationException as exception:
                print(exception.message_for_user)

            except TypeError as exception:
                error_message = str(exception)

                if "got an unexpected keyword argument" in error_message:
                    print("nieznany argument:", "--" + error_message.split("'")[1])

                elif "required positional argument" in error_message:
                    print("nie podano wymaganych opcji")

                elif (match := re.match(r".+(\d+) positional argument but (\d+).+", error_message)) is not None:
                    print("ta komenda wymaga {} opcji, a podano {}".format(
                        int(match.groups()[0]) - 1,
                        int(match.groups()[1]) - 1
                    ))
                else:
                    raise exception

            except KeyboardInterrupt as exception:
                continue
