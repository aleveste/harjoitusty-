# Arkkitehtuurikuvaus

## Rakenne

Ohjelma on jaettu kahteen alihakemistoon, ui, joka sisältää käyttöliittymää käsitteleviä luokkia (Game, BoardRenderer), ja game, joka sisältää sovelluslogiikkaa käsitteleviä luokkia (Board, Auth, GameLogic).

Alla on kaavio joka sisältää luokat, ja niiden yhteydet.

# Luokkakaavio

```mermaid
classDiagram
    class Game

    class AuthManager

    class Board

    class GameLogic {
    }

    class BoardRenderer

    Game --> AuthManager
    Game --> Board
    Game --> GameLogic
    Game --> BoardRenderer

    GameLogic --> Board
```

# Käyttöliittymä

Käyttöliittymässä on 4 eri näkymää. Kirjautuminen, missä voi rekisteröidä uuden käyttäjän, sekä kirjautua sisään. Tämän jälkeen pääsee valikkoon, missä voi valita pelimuodon kolmesta eri muodosta, pieni, medium ja iso. Tämän jälkeen siirrytään pelilaudalle, jonka koko riippuu valinnasta valikossa. Kun peli on päättynyt, voi halutessaan katsoa viimeaikaisia tuloksia tulosnäkymän avulla.

# Tietokanta

Tietokannassa on kaksi taulua, users ja scores. Users tallentaa rekisteröidyt käyttäjät, ja varmistaa, että kirjautuminen toimii ainoastaan silloin kun käyttäjä on jo olemassa. Scores tallentaa jokaisen pelin tuloksen niin, että omia tuloksia katsoessa ne eivät sekaannu muiden joukkoon, vaan ainoastaan omat tuokset näkyvät tulosnäkymässä.

# Sekvenssikaavio (Vasemman hiirinapin painallus pelikentällä)

```mermaid
sequenceDiagram
    participant User
    participant pygame
    participant Game
    participant Board
    participant BoardRenderer

    User->>pygame: Klikkaa hiiren vasemmalla
    pygame->>Game: Luo MOUSEBUTTONDOWN-tapahtuma
    Game->>Game: handle_events()
    Game->>Board: reveal(x, y)
    Board-->>Board: Merkitse solu paljastetuksi
    Board-->>Board: Rekursiivinen paljastus (jos arvo 0)
    Game->>BoardRenderer: draw(screen)
    BoardRenderer-->>BoardRenderer: Piirrä ruudut ruudulle
```
