import unittest
import sys
sys.path.append("src")
from board import Board
from game_logic import GameLogic

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.logic = GameLogic(grid_size=5, num_mines=0)

    def test_initial_state(self):
        self.assertFalse(self.logic.game_over)
        self.assertFalse(self.logic.game_lost)

    def test_left_click_win(self):
        self.logic.click(0, 0, 1)
        self.assertTrue(self.logic.game_over)
        self.assertFalse(self.logic.game_lost)

    def test_right_click_flags(self):
        self.logic.click(1, 1, 3)
        self.assertIn((1, 1), self.logic.board.flags)
        self.logic.click(1, 1, 3)
        self.assertNotIn((1, 1), self.logic.board.flags)

if __name__ == "__main__":
    unittest.main()
