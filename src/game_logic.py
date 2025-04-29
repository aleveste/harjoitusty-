# pylint: disable=import-error
from board import Board

class GameLogic:
    def __init__(self, grid_size, num_mines, cell_size=40):
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cell_size = cell_size
        self.game_over = False
        self.game_lost = False
        self.reset()

    def click(self, x, y, button):
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
        self.board = Board(self.grid_size, self.num_mines)
        self.game_over = False
        self.game_lost = False
        self.final_time = None

    def is_over(self):
        return self.game_over

    def is_lost(self):
        return self.game_lost

    def is_won(self):
        return self.game_over and not self.game_lost
