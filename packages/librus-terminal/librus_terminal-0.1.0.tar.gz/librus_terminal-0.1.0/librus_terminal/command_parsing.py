from shlex import split as split_command
from .exceptions import ParsingException


def parse_command(command: str) -> tuple[list, dict]:
    tokens = split_command(command)

    options, argument_tokens = [], []

    for index, token in enumerate(tokens):
        if token.startswith("--"):
            argument_tokens = tokens[index:]
            break

        options.append(token)

    prev_token, arguments = None, {}

    for token in argument_tokens:
        if token.startswith("--"):
            if prev_token is not None:
                arguments[prev_token.strip("--")] = True

            prev_token = token
            continue

        if prev_token is None:
            raise ParsingException("Options must be given before arguments:", [token])

        arguments[prev_token.strip("--")] = token

        prev_token = None

    if prev_token is not None:
        arguments[prev_token.strip("--")] = True

    return options, arguments
