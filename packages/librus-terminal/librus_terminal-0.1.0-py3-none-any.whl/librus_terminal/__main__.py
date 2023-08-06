from .librus_session import LibrusSession
from .librus_terminal import LibrusTerminal


def main():
    session = LibrusSession()

    terminal = LibrusTerminal(session)

    terminal.run_terminal()


if __name__ == "__main__":
    main()
