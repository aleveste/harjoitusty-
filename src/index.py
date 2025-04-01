import pygame
import random
from board import Board

GRID_SIZE = 10
CELL_SIZE = 40
NUM_MINES = 15

pygame.init()
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miinaharava")
board = Board()
running = True
game_over = False
while running:
    board.draw_board(screen)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if event.button == 1:  
                if (x, y) in board.mines:
                    board.reveal_cells(x, y)
                    game_over = True  
                else:
                    board.reveal_cells(x, y)
            elif event.button == 3:  
                if (x, y) in board.flags:
                    board.flags.remove((x, y))
                else:
                    board.flags.add((x, y))

pygame.quit()