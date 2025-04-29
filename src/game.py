# pylint: disable=import-error
import sys
import pygame
from game_logic import GameLogic
from board_render import BoardRenderer

class Game:
    """
    Luokka joka hallitsee peliä, ja vastaa sen logiikasta sekä käyttöliittymästä

    Attributes:
        logic (GameLogic): Pelin logiikka, joka sisältää pelilautan ja siihen liittyvät toiminnot.
        board_renderer (BoardRenderer): Pelilautaa piirtävä olio.
        width (int): Peliruudun leveys.
        height (int): Peliruudun korkeus.
        screen (pygame.Surface): Pygame-ikkuna, johon peli piirretään.
        font (pygame.font.Font): Fontti aikarajan ja pelitilanteen tekstille.
        start_ticks (int): Peliin kulunut aika millisekunneissa.
        final_time (int): Pelin päättymisaika sekuteina.
        game_lost (bool): Tieto siitä, onko peli hävitty.
        game_over (bool): Tieto siitä, onko peli päättynyt.
        running (bool): Tieto siitä, onko peli edelleen käynnissä.
        restart_rect (pygame.Rect): Painike, jota voidaan klikata uuden pelin aloittamiseksi.
        quit_rect (pygame.Rect): Painike, jota voidaan klikata pelistä poistumiseksi.  
    """
    def __init__(self):
        """
        Alustaa uuden pelin. Kysyy pelilaudan koon ja miinamäärän, jonka jälkeen se luo
        pelilogiikan sekä piirtojärjestelmän, ja asettaa peli-ikkunan sekä ajan.
        """
        pygame.init()
        self.grid_size, self.num_mines = self.ask_board_spec()

        self.logic = GameLogic(self.grid_size, self.num_mines)

        self.board_renderer = BoardRenderer(self.logic.board)

        self.width = self.grid_size * self.logic.board.cell_size
        self.height = self.grid_size * self.logic.board.cell_size + 100
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
        """
        Pyytää käyttäjältä pelilaudan koon ja miinojen määrän ennen pelin aloittamista.

        Returns:
            tuple: Palauttaa kaksi arvoa, jotka määrittävät pelilaudan koon (grid_size) 
            ja miinojen määrän (num_mines).
        """
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
        """
        Käynnistää pelin ja pitää sen käynnissä, kunnes peli on päättynyt.

        Metodi käsittelee piirtämisen sekä tapahtumakäsittelyn silmukan avulla.
        """
        while self.running:
            self.handle_draw()
            self.handle_events()

    def handle_draw(self):
        """
        Piirtää pelin tilan ruudulle, mukaan lukien pelilauta, aikaraja ja pelin päättymisviesti.

        Jos peli on päättynyt, piirtää pelin loppuviestin 
        ja vaihtoehdot uuden pelin aloittamiseksi tai pelistä poistumiseksi.
        """
        self.board_renderer.draw(self.screen)

        elapsed_time = ((pygame.time.get_ticks() - self.start_ticks) // 1000
                        if self.final_time is None else self.final_time)
        timer_text = self.font.render(f"Aika: {elapsed_time} s", True, (0, 0, 0))
        self.screen.blit(timer_text, (10, self.height - 30))

        if self.game_over:
            self.draw_end_screen()

        pygame.display.flip()

    def draw_end_screen(self):
        """
        Piirtää pelin loppuviestin ruudulle, joka ilmoittaa, onko peli voitettu vai hävitty.

        Tämä metodi piirtää myös painikkeet uuden pelin aloittamiseen tai pelistä poistumiseen.
        """
        color = (255, 0, 0) if self.game_lost else (0, 180, 0)
        message = "Häviö!" if self.game_lost else "Voitto!"
        status_text = self.font.render(message, True, color)
        self.screen.blit(status_text, (140, self.grid_size * self.logic.board.cell_size + 5))

        self.restart_rect = (pygame.Rect(50, self.grid_size *
                                         self.logic.board.cell_size + 35, 120, 30))
        self.quit_rect = pygame.Rect(230, self.grid_size * self.logic.board.cell_size + 35, 120, 30)

        pygame.draw.rect(self.screen, (0, 200, 0), self.restart_rect, border_radius=6)
        pygame.draw.rect(self.screen, (200, 0, 0), self.quit_rect, border_radius=6)

        restart_text = self.font.render("Uusi peli", True, (255, 255, 255))
        quit_text = self.font.render("Poistu", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.restart_rect.x + 10, self.restart_rect.y + 5))
        self.screen.blit(quit_text, (self.quit_rect.x + 25, self.quit_rect.y + 5))

    def handle_events(self):
        """
        Käsittelee kaikki pelissä tapahtuvat tapahtumat, 
        kuten käyttäjän syötteet ja ikkunan sulkemisen.

        Tämä metodi käsittelee hiiren klikkaukset ja näppäimistösyötteet, 
        kuten pelin uudelleenkäynnistyksen.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()

    def handle_mouse_click(self, event):
        """
        Käsittelee käyttäjän hiiren klikkaukset pelilautaa klikatessa.

        Args:
            event (pygame.event.Event): Pygame-tapahtuma, joka sisältää tiedot hiiren klikkauksesta.
        """
        x, y = (event.pos[0] // self.logic.board.cell_size, event.pos[1] //
                self.logic.board.cell_size)

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
        """
        Käsittelee pelilautaa klikkaamisen ja tarkistaa, 
        onko peli päättynyt tai voittaminen mahdollista.

        Args:
            x (int): Pelilaudan x-koordinaatti.
            y (int): Pelilaudan y-koordinaatti.
            button (int): Painettu hiiren nappi (vasen tai oikea).
        """
        if button == 1:
            if (x, y) in self.logic.board.mines:
                self.logic.board.reveal(x, y)
                self.game_over = True
                self.final_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                self.game_lost = True
            else:
                self.logic.board.reveal(x, y)
                if self.logic.board.check_win():
                    self.game_over = True
                    self.final_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                    self.game_lost = False
        elif button == 3:
            if (x, y) in self.logic.board.flags:
                self.logic.board.flags.remove((x, y))
            else:
                self.logic.board.flags.add((x, y))

    def reset_game(self):
        """
        Nollaa pelin ja aloittaa uuden pelin alkuperäisillä asetuksilla.

        Metodi luo uuden pelin ja päivittää pelin tilan sekä piirtojärjestelmän.
        """
        self.logic = GameLogic(self.grid_size, self.num_mines)
        self.board_renderer = BoardRenderer(self.logic.board)
        self.game_over = False
        self.game_lost = False
        self.start_ticks = pygame.time.get_ticks()
        self.final_time = None


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
