import pygame
from game.auth import AuthManager

auth = AuthManager()

pygame.init()
FONT = pygame.font.Font(None, 36)
WIDTH, HEIGHT = 500, 300
WHITE, BLACK, GRAY, RED, GREEN = (255, 255, 255), (0, 0, 0), (200, 200, 200), (255, 0, 0), (0, 200, 0)

class InputBox:
    def __init__(self, x, y, w, h, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = ''
        self.txt_surface = FONT.render('', True, self.color)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                self.text += event.unicode
        self.txt_surface = FONT.render(
            '*' * len(self.text) if self.is_password else self.text, True, self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def get_text(self):
        return self.text

def login_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kirjautuminen")

    username_box = InputBox(250, 50, 200, 40)
    password_box = InputBox(250, 110, 200, 40, is_password=True)

    login_button = pygame.Rect(100, 180, 120, 40)
    register_button = pygame.Rect(280, 180, 120, 40)

    clock = pygame.time.Clock()
    message = ''
    message_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            username_box.handle_event(event)
            password_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    if username_box.get_text() == "" or password_box.get_text() == "":
                        message = "Tunnus ja salasana eivät voi olla tyhjiä"
                        message_color = RED
                    else:
                        if auth.login_user(username_box.get_text(), password_box.get_text()):
                            return username_box.get_text()
                        else:
                            message = "Virheellinen tunnus tai salasana"
                            message_color = RED
                elif register_button.collidepoint(event.pos):
                    if username_box.get_text() == "" or password_box.get_text() == "":
                        message = "Tunnus ja salasana eivät voi olla tyhjiä"
                        message_color = RED
                    else:
                        if auth.register_user(username_box.get_text(), password_box.get_text()):
                            message = "Rekisteröinti onnistui"
                            message_color = GREEN
                        else:
                            message = "Tunnus on jo olemassa"
                            message_color = RED

        screen.fill(WHITE)

        screen.blit(FONT.render("Käyttäjätunnus:", True, BLACK), (30, 60))
        screen.blit(FONT.render("Salasana:", True, BLACK), (30, 120))
        screen.blit(FONT.render(message, True, message_color), (30, 240))

        username_box.draw(screen)
        password_box.draw(screen)

        pygame.draw.rect(screen, GRAY, login_button)
        pygame.draw.rect(screen, GRAY, register_button)
        screen.blit(FONT.render("Kirjaudu", True, BLACK), (login_button.x + 15, login_button.y + 5))
        screen.blit(FONT.render("Rekisteröidy", True, BLACK), (register_button.x + 5, register_button.y + 5))

        pygame.display.flip()
        clock.tick(30)
