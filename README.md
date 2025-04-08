[Työaikakirjanpito](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/tuntikirjanpito.md)

[Vaatimusmäärittely](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Changelog](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/changelog.md)

## Asennus

1. Asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komennot

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _htmlcov_-hakemistoon.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```
