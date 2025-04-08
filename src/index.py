import pygame
from board import Board
# pylint: disable=invalid-name

start_ticks = pygame.time.get_ticks()
final_time = None
game_lost = False

pygame.init()
temp_board = Board(10, 15)
GRID_SIZE, NUM_MINES = temp_board.ask_board_spec()
board = Board(GRID_SIZE, NUM_MINES)
CELL_SIZE = board.cell_size
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miinaharava")
running = True
game_over = False
while running:
    board.draw_board(screen)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    if final_time is None:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    else:
        elapsed_time = final_time
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Aika: {elapsed_time} s", True, (0, 0, 0))
    screen.blit(timer_text, (10, HEIGHT - 30))
    if game_over:
        if game_lost:
            text = font.render("Häviö! Uusi peli = R", True, (255, 0, 0))
        else:
            text = font.render("Voitto! Uusi peli = R", True, (0, 180, 0))
        screen.blit(text, (130, board.grid_size * CELL_SIZE + 10))
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
                    final_time = (pygame.time.get_ticks() - start_ticks) // 1000
                    game_lost = True
                else:
                    board.reveal_cells(x, y)
                    if board.check_for_win():
                        game_over = True
                        final_time = (pygame.time.get_ticks() - start_ticks) // 1000
                        game_lost = False
            elif event.button == 3:
                if (x, y) in board.flags:
                    board.flags.remove((x, y))
                else:
                    board.flags.add((x, y))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = Board(GRID_SIZE, NUM_MINES)
                game_over = False
                game_lost = False
                start_ticks = pygame.time.get_ticks()
                final_time = None

pygame.quit()
