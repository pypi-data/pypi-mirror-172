from .librus_session import LibrusSession


def help_command(session: LibrusSession) -> None:
    message = """
Librus terminal

Komendy:

    gmes - pobiera, wyświetla i zapisuje w pamięci programu listę wiadomosci w następującym formacie: IndeksWiadomości InformacjeDodatkowe Data Nadawca Temat
        Użycie:
            gmes <arguments>
                arguments:
                    - --source [options] - skąd mają być pobrane wiadomosci, opcje to:
                        - archive - wiadomosci będą pobrane z archiwum
                        - current - wiadomosci z aktualnego roku szkolnego
                        - mamory - wiadomosci zapisane w pamięci programu
                    - --person nazwisko - wiadomosci od jakiej osoby mają być wyświetlone. Trzeba podac nazwisko osoby (lub jego część)
                    - --pages pages - z jakich stron mają być pobrane wiadomosci. Format to PierwszStrona-OstatniaStrona, np 2-4 pobierze strony 2, 3 i 4

    exit - zamyka program

    cls - czyści ekran

    login - loguje do librusa
        Użycie:
            login <arguments>
                arguments:
                    - --login login - login do librusa
                    - --password password - hasło do librusa

    logout - wylogowuje

    rmes - odczytuje wiadomość zapisaną w pamięci programu. Wcześniej trzeba użyć komendy gmes która zapisuje wiadomosci w pamięci
        Użycie:
            rmes indeks
                options:
                    - indeks - indeks wiadomosci którą chcemy odczytać.

    help - wyświetla tą wiadomosć
"""

    print(message)
