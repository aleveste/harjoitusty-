import pygame
import random

GRID_SIZE = 10
CELL_SIZE = 40
NUM_MINES = 15

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.font.init()
FONT = pygame.font.Font(None, 30)

class Board:
    def __init__(self):
        self.board, self.mines = self.create_board()
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flags = set()

    def create_board(self):
        board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        mines = set()
    
        while len(mines) < NUM_MINES:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                board[y][x] = -1  
    

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board[y][x] == -1:
                    continue
                count = sum((nx, ny) in mines for nx in range(x-1, x+2) for ny in range(y-1, y+2) if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE)
                board[y][x] = count
    
        return board, mines
    
    def draw_board(self, screen):
        screen.fill(WHITE)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if self.board[y][x] > 0:
                        text = FONT.render(str(self.board[y][x]), True, BLACK)
                        screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))
                    elif self.board[y][x] == -1:
                        pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 3)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if (x, y) in self.flags:
                        pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def reveal_cells(self, x, y):
        if self.revealed[y][x] or (x, y) in self.flags:
            return
        self.revealed[y][x] = True
        if self.board[y][x] == 0:
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        self.reveal_cells(nx, ny)