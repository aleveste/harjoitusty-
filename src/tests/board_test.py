import unittest
import sys
sys.path.append("src")
from game.board import Board

class TestMiinaharava(unittest.TestCase):

    def setUp(self):
        self.board = Board(grid_size=5, num_mines=3)

    def test_board_dimensions(self):
        self.assertEqual(len(self.board.board), 5)
        self.assertEqual(len(self.board.board[0]), 5)

    def test_number_of_mines(self):
        mine_count = sum(cell == -1 for row in self.board.board for cell in row)
        self.assertEqual(mine_count, 3)
        self.assertEqual(len(self.board.mines), 3)

    def test_reveal_non_mine(self):
        for y in range(5):
            for x in range(5):
                if (x, y) not in self.board.mines:
                    self.board.reveal(x, y)
                    self.assertTrue(self.board.revealed[y][x])
                    return

    def test_reveal_is_idempotent(self):
        self.board.revealed[0][0] = True
        self.board.reveal(0, 0)
        self.assertTrue(self.board.revealed[0][0])

    def test_check_win_false_initially(self):
        self.assertFalse(self.board.check_win())

    def test_check_win_true_when_all_non_mines_revealed(self):
        for y in range(5):
            for x in range(5):
                if (x, y) not in self.board.mines:
                    self.board.revealed[y][x] = True
        self.assertTrue(self.board.check_win())

    def test_flagging(self):
        self.assertEqual(len(self.board.flags), 0)
        self.board.flags.add((1, 1))
        self.assertIn((1, 1), self.board.flags)
        self.board.flags.remove((1, 1))
        self.assertNotIn((1, 1), self.board.flags)

if __name__ == "__main__":
    unittest.main()
