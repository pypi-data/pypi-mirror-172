from .librus_session import LibrusSession
import librus_scraper
import re


def _ljust_with_dots(string: str, length: int, fillchar: str = " ", inc_space: bool = True) -> int:
    if len(string) <= length:
        return string.ljust(length, fillchar) + " " * inc_space

    else:
        return string[:length - 3] + "..." + " " * inc_space


def print_message(index: int, mes: dict) -> None:

    string = \
        _ljust_with_dots(str(index), 4, inc_space=0) +\
        (("P" * mes["files"]) or " ") + (("N " * mes["new"]) or "  ") +\
        mes["data"].split(" ")[0] + " " +\
        _ljust_with_dots(mes["nadawca"].split("(")[0], 20) +\
        _ljust_with_dots(mes["temat"], 60)

    print(string)


def print_messages(messages: list[dict], pages: list[int] = None) -> None:
    for index, message in enumerate(messages):
        print_message(index + 1, message)

    if pages is not None:
        print("{}-{}/{}".format(*pages))


def get_messages_command(
    session: LibrusSession, *, source: str = "current", person: str = "-", pages: str = None
) -> int:

    if source == "current":
        archive = False

    elif source == "archive":
        archive = True

    elif source == "memory":
        if session.messages is None:
            print("nie ma wiadomości zapisanych w pamięci")
            return 1

        print_messages(session.messages, pages=session.messages_pages)

        return 0

    else:
        print("nieznane źródło wiadomości")
        return 1

    if person != "-":
        people = librus_scraper.messages.get_senders_id(session.cookies, archive=archive)

        for person_id, person_name in people[1:]:
            if person_name.lower().startswith(person.lower()):
                person = person_id
                break

        else:
            print("nie ma takiej osoby")
            return 1

    if pages is None:
        pages = "1-1"

    match = re.match(r"^(\d{0,})-(\d{0,})$", pages)

    if match is None:
        print("niepoprawny format stron (np. 1-10)")
        return 1

    page_range = [
        int(match.groups()[0]) if match.groups()[0] else None,
        int(match.groups()[1]) if match.groups()[1] else None,
    ]

    pagination = [
        (page_range[0] - 1) if page_range[0] is not None else 0
    ]

    pagination.append(pagination[0] + 1)

    messages: list[dict] = []

    pages: list[int] = [
        page_range[0] if page_range[0] is not None else 1, 0, 0
    ]

    while pagination[0] < pagination[1]:
        if page_range[1] is not None and pagination[0] >= page_range[1]:
            break

        result = librus_scraper.messages.get_messages(
            cookies=session.cookies,
            archive=archive,
            person=person,
            page=str(pagination[0])
        )

        pagination = result["pagination"]

        pages = [
            min(pagination[0], pages[0]),
            max(pages[1], pagination[0]),
            pagination[1]
        ]

        messages += result["messages"]

        if page_range[0] is not None and pagination[1] < page_range[0]:
            break

    if not messages:
        print("żadne wiadomości nie spełniają tych warunków")
        return 1

    session.messages = messages
    session.messages_pages = pages

    print_messages(session.messages, pages=session.messages_pages)


def read_message_command(session: LibrusSession, index: str) -> int:
    if session.messages is None:
        print("nie ma wiadomości w pamięci")
        return 1

    match = re.match(r"^\d+$", index)

    if match is None:
        print(index, "nie jest liczbą")
        return 1

    index = int(index) - 1

    if index not in range(len(session.messages)):
        print("nie ma wiadomości o takim indeksie")
        return 1

    message = librus_scraper.read_message(session.cookies, session.messages[index]["href"])

    print("Nadawca:", message["nadawca"])
    print("Data:", message["data"])
    print("Temat:", message["temat"], "\n")
    print(message["tresc"])
