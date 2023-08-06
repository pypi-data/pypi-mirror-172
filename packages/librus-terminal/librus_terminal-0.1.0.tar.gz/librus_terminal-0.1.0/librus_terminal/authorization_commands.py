from .librus_session import LibrusSession
from .exceptions import TerminalAuthorizationException
from librus_scraper.authorization import AuthorizationException as LibrusAuthException
import json


def logout_command(session: LibrusSession) -> None:
    session._cookies = None
    session._cookie_session_expires = 0
    session._csrf_token = None


def login_command(session: LibrusSession, *, login: str = None, password: str = None) -> None:

    while not login:
        login = input("[login] >> ")

    while not password:
        password = input("[password] >> ")

    try:
        session.login(login, password)

    except LibrusAuthException:
        raise TerminalAuthorizationException("invalid login or password", "nieprawidłowe hasło lub login")
