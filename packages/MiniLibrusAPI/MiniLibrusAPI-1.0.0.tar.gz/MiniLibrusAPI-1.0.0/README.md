# MiniLibrusAPI
![PyPI Python Version](https://img.shields.io/pypi/pyversions/fortnite-api?label=python%20version&logo=python&logoColor=yellow)
[![discord server invite](https://discordapp.com/api/guilds/881251978951397396/embed.png)](https://discord.com/invite/pFUTyqqcUx)

Łatwy do użycia moduł MiniLibrusAPI.


## Instalacja

Wymagany jest Python 3.5 lub lepszy.

```
pip install MiniLibrusAPI
```


## Dokumentacja

Na początek musimy zaimportować api.

```
from MiniLibrusAPI import Librus
```


### Logowanie

Potem musimy się zalogować.

```
Librus.login(login="", haslo="")
```

Po zalogowaniu możemy korzystać z api.


### Szczesliwy numerek

Zwraca szczesliwy numerek

```
Librus.szczesliwy_numerek()
```


### Informacje

Zwraca informacje

```
Librus.informacje.uczen()
Librus.informacje.klasa()
Librus.informacje.numer_w_dzienniku()
Librus.informacje.wychowawca()
```