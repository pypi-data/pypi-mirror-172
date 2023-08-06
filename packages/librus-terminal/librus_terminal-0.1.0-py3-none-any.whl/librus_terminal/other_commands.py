from .librus_session import LibrusSession
import os


def exit_command(session: LibrusSession) -> None:
    exit()


def clear_command(session: LibrusSession) -> None:
    os.system("cls")
