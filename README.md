# Miinaharava

Sovelluksen sisällä käyttäjät voivat pelata kuuluisaa peliä miinaharavaa, missä tavoitteena on tyhjentää pelilauta tyhjistä ruuduista, jättämällä miinoitetut ruudut koskematta. Käyttäjä voi kirjautua sisään, ja nähdä pelihistorian, joka sisältää ajan, lopputuloksen, sekä pelilaudan koon.

## Huomio Python-versiosta

Sovellusta on testattu versiolla 3.10, sitä vanhemmilla versiolla voi esiintyä ongelmia.

[Työaikakirjanpito](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/tuntikirjanpito.md)

[Vaatimusmäärittely](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Changelog](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/changelog.md)

[Arkkitehtuuri](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/arkkitehtuuri.md)

[Käyttöohje](https://github.com/aleveste/harjoitusty-/blob/main/dokumentaatio/kayttoohje.md)

[Release](https://github.com/aleveste/harjoitusty-/releases)

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
