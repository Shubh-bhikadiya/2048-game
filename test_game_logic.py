import unittest
import game_logic


class GameLogicTests(unittest.TestCase):

    def setUp(self):
        # Start each test with a clean score and move status.
        game_logic.score = 0
        game_logic.check = False

    def test_left_move_merges_two_equal_tiles(self):
        board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        result = game_logic.move_left(board)

        expected = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        self.assertEqual(result, expected)
        self.assertEqual(game_logic.score, 4)

    def test_one_tile_cannot_merge_twice_in_one_move(self):
        board = [
            [2, 2, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        result = game_logic.move_left(board)

        expected = [
            [4, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        self.assertEqual(result, expected)
        self.assertEqual(game_logic.score, 8)

    def test_move_right_moves_tile_to_right_side(self):
        board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        result = game_logic.move_right(board)

        expected = [
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        self.assertEqual(result, expected)

    def test_move_that_changes_nothing_is_detected(self):
        board = [
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        result = game_logic.move_left(board)

        self.assertEqual(result, board)
        self.assertFalse(game_logic.check)
        self.assertEqual(game_logic.score, 0)

    def test_game_win_is_detected(self):
        board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 2],
            [0, 0, 0, 0],
        ]

        self.assertTrue(game_logic.Game_win(board))

    def test_game_over_when_board_is_full_and_no_tiles_match(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]

        self.assertTrue(game_logic.Game_over(board))


if __name__ == "__main__":
    unittest.main()