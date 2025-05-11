# pylint: disable=invalid-name
import random

class Board:
    """
    Pelilauta, joka vastaa miinakentän luomisesta, pelitilan tarkistamisesta ja pelin logiikasta.

    Attributes:
        grid_size (int): Pelilaudan koko.
        num_mines (int): Miinojen määrä pelissä.
        cell_size (int): Yhden peliruudun koko pikseleinä.
        board (list of list of int): Pelilauta, jossa on miinat (-1) 
        ja numerot (0-8) miinojen ympärillä.
        mines (set of tuple): Setti, joka sisältää miinojen sijainnit (x, y).
        revealed (list of list of bool): Lista, joka seuraa, mitkä ruudut on paljastettu.
        flags (set of tuple): Setti, joka sisältää ruudut, joihin käyttäjä on asettanut lipun.
    """
    def __init__(self, grid_size, num_mines, cell_size=40):
        """
        Alustaa pelilaudan ja asettaa miinat ja numerot pelilaudalle.

        Args:
            grid_size (int): Pelilaudan koko.
            num_mines (int): Miinojen määrä pelissä.
        """
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cell_size = cell_size
        self.board, self.mines = self.create_board()
        self.revealed = [[False] * grid_size for _ in range(grid_size)]
        self.flags = set()

    def create_board(self):
        """
        Luo pelilaudan ja asettaa miinat satunnaisesti randomin avulla. 
        Laskee miinojen ympärillä olevat numerot.

        Returns:
            tuple: Palauttaa kaksi arvoa:
                - board (list of list of int): Pelilauta, jossa on miinat (-1) ja numerot (0-8).
                - mines (set of tuple): Setti, joka sisältää miinojen sijainnit.
        """
        board = [[0] * self.grid_size for _ in range(self.grid_size)]
        mines = set()

        while len(mines) < self.num_mines:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                board[y][x] = -1

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if board[y][x] == -1:
                    continue
                count = sum((nx, ny) in mines for nx in range(x-1, x+2) for ny in range(y-1, y+2)
                            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size)
                board[y][x] = count

        return board, mines

    def is_mine(self, x, y):
        """
        Tarkistaa, onko pelissä kyseinen ruutu miina.

        Args:
            x (int): Pelilaudan x-koordinaatti.
            y (int): Pelilaudan y-koordinaatti.

        Returns:
            bool: True, jos kyseessä on miina, muuten False.
        """
        return (x, y) in self.mines

    def reveal(self, x, y):
        """
        Paljastaa pelilautaa tietyssä kohdassa ja paljastaa ympäröivät solut, 
        jos kyseessä on tyhjä solu.

        Jos ruudussa on numero 0, paljastaa kaikki siihen liittyvät tyhjät solut.
        Jos ruudussa on miina, peli päättyy.

        Args:
            x (int): Pelilaudan x-koordinaatti.
            y (int): Pelilaudan y-koordinaatti.
        """
        if self.revealed[y][x] or (x, y) in self.flags:
            return
        self.revealed[y][x] = True
        if self.board[y][x] == 0:
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        self.reveal(nx, ny)

    def toggle_flag(self, x, y):
        """
        Vaihtaa lipun tilan pelilaudan tietyssä solussa.

        Jos solussa ei ole lippua, se lisätään. Jos siinä on lippu, se poistetaan.

        Args:
            x (int): Pelilaudan x-koordinaatti.
            y (int): Pelilaudan y-koordinaatti.
        """
        if (x, y) in self.flags:
            self.flags.remove((x, y))
        else:
            self.flags.add((x, y))

    def check_win(self):
        """
        Tarkistaa, onko pelaaja voittanut pelin.

        Voitto saavutetaan, kun kaikki miinattomat ruudut on paljastettu.

        Returns:
            bool: True, jos peli on voitettu, muuten False.
        """
        return all(
            self.revealed[y][x] or (x, y) in self.mines
            for y in range(self.grid_size)
            for x in range(self.grid_size)
        )
