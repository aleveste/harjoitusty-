# pylint: disable=import-error
from game.board import Board

class GameLogic:
    """
    GameLogic hallitsee pelin ydintoimintoja kuten klikkauksia,
    pelin voitto tai häviö, ja pelin nollaamisen.

    Attributes:
        grid_size (int): Peliruudukon koko.
        num_mines (int): Miinojen määrä.
        cell_size (int): Solun pikselikoko käyttöliittymässä.
        game_over (bool): Onko peli päättynyt.
        game_lost (bool): Hävisikö pelaaja pelin.
        board (Board): Pelilauta-olio.
        final_time (int | None): Päättymisaika sekunteina.
    """
    def __init__(self, grid_size, num_mines, cell_size=40):
        """
        Alustaa GameLogic-olion ja uuden pelin.

        Args:
            grid_size (int): Ruudukon koko.
            num_mines (int): Miinojen määrä.
            cell_size (int): Solun koko pikseleinä.
        """
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cell_size = cell_size
        self.game_over = False
        self.game_lost = False
        self.reset()

    def click(self, x, y, button):
        """
        Käsittelee hiiren klikkauksen annetussa ruudussa.

        Args:
            x (int): X-koordinaatti.
            y (int): Y-koordinaatti.
            button (int): Hiiren painike.
        """
        if self.game_over:
            return

        if button == 1:
            if (x, y) in self.board.mines:
                self.board.reveal(x, y)
                self.game_over = True
                self.game_lost = True
            else:
                self.board.reveal(x, y)
                if self.board.check_win():
                    self.game_over = True
                    self.game_lost = False
        elif button == 3:
            if (x, y) in self.board.flags:
                self.board.flags.remove((x, y))
            else:
                self.board.flags.add((x, y))

    def reset(self):
        """
        Nollaa pelin luomalla uuden Board-olion ja asettamalla pelitilat alkutilaan.
        """
        self.board = Board(self.grid_size, self.num_mines)
        self.game_over = False
        self.game_lost = False
        self.final_time = None

    def is_over(self):
        """
        Tarkistaa, onko peli päättynyt.

        Returns:
            bool: True jos peli on ohi, muuten False.
        """
        return self.game_over

    def is_lost(self):
        """
        Tarkistaa, hävisikö pelaaja pelin.

        Returns:
            bool: True jos peli on hävitty, muuten False.
        """
        return self.game_lost

    def is_won(self):
        """
        Tarkistaa, voittiko pelaaja pelin.

        Returns:
            bool: True jos peli on voitettu, muuten False.
        """
        return self.game_over and not self.game_lost
