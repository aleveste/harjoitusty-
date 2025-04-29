import pygame

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.font.init()
FONT = pygame.font.Font(None, 30)

class BoardRenderer:
    def __init__(self, board, cell_size=40):
        self.board = board
        self.cell_size = cell_size

    def draw(self, screen):
        screen.fill(WHITE)
        for y in range(self.board.grid_size):
            for x in range(self.board.grid_size):
                rect = (pygame.Rect(x * self.cell_size, y *
                                    self.cell_size, self.cell_size, self.cell_size))

                if self.board.revealed[y][x]:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                    if self.board.board[y][x] > 0:
                        text = FONT.render(str(self.board.board[y][x]), True, BLACK)
                        screen.blit(text, (rect.x + 10, rect.y + 5))
                    elif self.board.board[y][x] == -1:
                        pygame.draw.circle(screen, RED, rect.center, self.cell_size // 3)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if (x, y) in self.board.flags:
                        pygame.draw.circle(screen, BLACK, rect.center, self.cell_size // 4)

                pygame.draw.rect(screen, BLACK, rect, 1)
