# pylint: disable=import-error
from game.auth import AuthManager
from ui.login_screen import login_screen
from ui.game import Game

auth = AuthManager()

def main():
    auth.create_user_table()
    auth.create_score_table()

    username = login_screen()
    if username:
        game = Game(username)
        game.run()

if __name__ == "__main__":
    main()
