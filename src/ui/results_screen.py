import pygame
from game.auth import AuthManager

auth = AuthManager()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 24)

def show_results_screen(screen, username):
    results = auth.get_user_scores(username)

    screen.fill(WHITE)

    title = FONT.render(f"{username} – Viimeisimmät pelit", True, BLACK)
    screen.blit(title, (20, 20))

    for i, (grid_size, duration, won, played_at) in enumerate(results):
        status = "Voitto" if bool(won) else "Häviö"
        line = f"{grid_size}×{grid_size} – {status} – {duration}s – {played_at[:19]}"
        text = FONT.render(line, True, BLACK)
        screen.blit(text, (20, 60 + i * 30))

    back_text = FONT.render("Paina ESC palataksesi", True, BLACK)
    screen.blit(back_text, (20, 400))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False