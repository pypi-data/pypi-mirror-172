# Librus synergia terminal
Aplikacja działająca w terminalu, służąca do pobierania najważniejszych informacji z dziennika elektronicznego Librus Synergia.

## Funkcje
- pobieranie listy wiadomości
- odczytywanie poszczególnych wiadomości

## Wymagania
Biblioteka [librus scraper](https://github.com/piotr-ginal/librus-scraper)
## Instalacja
```bash
pip install -e .
```
## Wygląd interfejsu
![interfejs](https://user-images.githubusercontent.com/70772418/197017415-7e059be5-fee1-44fa-9607-f2a9f4a5b7b6.png)
## Komendy
```
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
```
## Przykłady użycia
- ```login --login 890921u --password qwerty123``` - loguje danego użytkownika do systemu
- ```gmes --source archive --person kowalski --pages 4-7``` - pobiera i zapisuje archiwalne wiadomości od nauczyciela o nazwisku kowalski, ze stron 4, 5, 6 i 7
- ```rmes 5``` - odczytuje 5 wiadomości z pamięci.