import unittest
import sys
sys.path.append("src")
from board import Board, NUM_MINES, GRID_SIZE

class TestMiinaharava(unittest.TestCase):
    def setUp(self):
        self.board_instance = Board()

    def test_mines(self):
        board, mines = self.board_instance.create_board()

        self.assertEqual(len(mines), NUM_MINES)

        for x, y in mines:
            self.assertTrue(0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE)
            self.assertEqual(board[y][x], -1)

if __name__ == "__main__":
    unittest.main()