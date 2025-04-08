```mermaid
classDiagram
    class Game 

    class Board 

    class UI

    class User

    Game --> User
    Game --> Board
    Game --> UI
    Board --> UI
```