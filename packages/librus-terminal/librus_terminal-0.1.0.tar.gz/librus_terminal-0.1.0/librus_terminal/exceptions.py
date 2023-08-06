class ParsingException(Exception):
    def __init__(self, message, errors) -> None:
        super().__init__(message)

        self.errors = errors


class TerminalAuthorizationException(Exception):
    def __init__(self, message, message_for_user) -> None:
        super().__init__(message)

        self.message_for_user = message_for_user
