from librus_terminal.command_parsing import parse_command
import librus_scraper
from .exceptions import TerminalAuthorizationException
import time


class LibrusSession():

    minimum_left = 10

    def __init__(self) -> None:
        self._cookies = None
        self._csrf_token = None

        self.messages = None
        self.messages_pages = None

        self._cookie_session_expires = 0

    def login(self, login: str, password: str) -> None:
        cookies = librus_scraper.authorization._get_cookies(login, password)

        expires = 0

        for cookie in cookies:
            if cookie.name != "oauth_token":
                continue

            expires = cookie.expires
            break

        self._cookies = dict(cookies)

        self._cookie_session_expires = expires

        self._csrf_token = librus_scraper.get_csrf_token(self.cookies)

    def check_if_expired(self) -> None:
        time_left = self._cookie_session_expires - round(time.time())

        if time_left < self.minimum_left:
            raise TerminalAuthorizationException(
                "cookies expired", "sesja wygasła, musisz się ponownie zalogować"
            )

    @property
    def cookies(self) -> dict:
        if self._cookies is not None:
            self.check_if_expired()
            return self._cookies

        raise TerminalAuthorizationException(
            "no cookies for this session", "musisz się zalogowac"
        )

    @property
    def csrf_token(self) -> str:
        if self._csrf_token is not None:
            self.check_if_expired()
            return self._csrf_token

        raise TerminalAuthorizationException(
            "no csrf_token for this session", "musisz się zalogowac"
        )
