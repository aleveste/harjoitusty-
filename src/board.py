import random
import pygame
# pylint: disable=invalid-name
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.font.init()
FONT = pygame.font.Font(None, 30)


class Board:
    def __init__(self, grid_size, num_mines):
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.cell_size = 40
        self.board, self.mines = self.create_board()
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flags = set()

    def create_board(self):
        board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        mines = set()

        while len(mines) < self.num_mines:
            x, y = random.randint(
                0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                board[y][x] = -1

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if board[y][x] == -1:
                    continue
                count = sum((nx, ny) in mines for nx in range(
                    x-1, x+2) for ny in range(y-1, y+2) if 0 <= nx < self.grid_size
                    and 0 <= ny < self.grid_size)
                board[y][x] = count

        return board, mines

    def draw_board(self, screen):
        screen.fill(WHITE)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y *
                                   self.cell_size, self.cell_size, self.cell_size)
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if self.board[y][x] > 0:
                        text = FONT.render(str(self.board[y][x]), True, BLACK)
                        screen.blit(
                            text, (x * self.cell_size + 10, y * self.cell_size + 5))
                    elif self.board[y][x] == -1:
                        pygame.draw.circle(
                            screen, RED, rect.center, self.cell_size // 3)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if (x, y) in self.flags:
                        pygame.draw.circle(
                            screen, BLACK, rect.center, self.cell_size // 4)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def reveal_cells(self, x, y):
        if self.revealed[y][x] or (x, y) in self.flags:
            return
        self.revealed[y][x] = True
        if self.board[y][x] == 0:
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        self.reveal_cells(nx, ny)

    def check_for_win(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if (x, y) not in self.mines and not self.revealed[y][x]:
                    return False
        return True
    