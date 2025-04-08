import unittest
import sys
sys.path.append("src")
from board import Board

class TestMiinaharava(unittest.TestCase):
    def setUp(self):
        self.board_instance = Board(10, 15)

    def test_mines(self):
        board, mines = self.board_instance.create_board()

        self.assertEqual(len(mines), 15)

        for x, y in mines:
            self.assertTrue(0 <= x < 10 and 0 <= y < 10)
            self.assertEqual(board[y][x], -1)

if __name__ == "__main__":
    unittest.main()
