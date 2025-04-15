# pylint: disable=import-error
import sys
import pygame
from board import Board
class Game:
    def __init__(self):
        pygame.init()
        self.grid_size, self.num_mines = self.ask_board_spec()
        self.board = Board(self.grid_size, self.num_mines)
        self.cell_size = self.board.cell_size
        self.width = self.grid_size * self.cell_size
        self.height = self.grid_size * self.cell_size + 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Miinaharava")
        self.font = pygame.font.Font(None, 36)

        self.start_ticks = pygame.time.get_ticks()
        self.final_time = None
        self.game_lost = False
        self.game_over = False
        self.running = True
        self.restart_rect = None
        self.quit_rect = None

    def ask_board_spec(self):
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Valitse pelilaudan koko")
        font = pygame.font.Font(None, 36)

        options = [
            ("Pieni (10x10)", 10, 15),
            ("Medium (15x15)", 15, 45),
            ("Iso (20x20)", 20, 75)
        ]

        buttons = []
        for i, (label, _, _) in enumerate(options):
            text = font.render(label, True, (255, 255, 255))
            rect = pygame.Rect(100, 50 + i * 70, 200, 50)
            buttons.append((text, rect))

        while True:
            screen.fill((30, 30, 30))

            for text, rect in buttons:
                pygame.draw.rect(screen, (70, 70, 200), rect, border_radius=8)
                screen.blit(text, (rect.x + 10, rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i, (_, width, mines) in enumerate(options):
                        if buttons[i][1].collidepoint(mx, my):
                            return width, mines

    def run(self):
        while self.running:
            self.handle_draw()
            self.handle_events()

    def handle_draw(self):
        self.board.draw_board(self.screen)

        elapsed_time = ((pygame.time.get_ticks() - self.start_ticks) // 1000
                        if self.final_time is None else self.final_time)
        timer_text = self.font.render(f"Aika: {elapsed_time} s", True, (0, 0, 0))
        self.screen.blit(timer_text, (10, self.height - 30))

        if self.game_over:
            self.draw_end_screen()

        pygame.display.flip()

    def draw_end_screen(self):
        color = (255, 0, 0) if self.game_lost else (0, 180, 0)
        message = "Häviö!" if self.game_lost else "Voitto!"
        status_text = self.font.render(message, True, color)
        self.screen.blit(status_text, (140, self.grid_size * self.cell_size + 5))

        self.restart_rect = pygame.Rect(50, self.grid_size * self.cell_size + 35, 120, 30)
        self.quit_rect = pygame.Rect(230, self.grid_size * self.cell_size + 35, 120, 30)

        pygame.draw.rect(self.screen, (0, 200, 0), self.restart_rect, border_radius=6)
        pygame.draw.rect(self.screen, (200, 0, 0), self.quit_rect, border_radius=6)

        restart_text = self.font.render("Uusi peli", True, (255, 255, 255))
        quit_text = self.font.render("Poistu", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.restart_rect.x + 10, self.restart_rect.y + 5))
        self.screen.blit(quit_text, (self.quit_rect.x + 25, self.quit_rect.y + 5))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()

    def handle_mouse_click(self, event):
        x, y = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size

        if self.game_over:
            if self.restart_rect.collidepoint(event.pos):
                self.running = False
                new_game = Game()
                new_game.run()
            elif self.quit_rect.collidepoint(event.pos):
                self.running = False
        else:
            self.handle_board_click(x, y, event.button)

    def handle_board_click(self, x, y, button):
        if button == 1:
            if (x, y) in self.board.mines:
                self.board.reveal_cells(x, y)
                self.game_over = True
                self.final_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                self.game_lost = True
            else:
                self.board.reveal_cells(x, y)
                if self.board.check_for_win():
                    self.game_over = True
                    self.final_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                    self.game_lost = False
        elif button == 3:
            if (x, y) in self.board.flags:
                self.board.flags.remove((x, y))
            else:
                self.board.flags.add((x, y))

    def reset_game(self):
        self.board = Board(self.grid_size, self.num_mines)
        self.game_over = False
        self.game_lost = False
        self.start_ticks = pygame.time.get_ticks()
        self.final_time = None
