# imports
import unittest
import random
import project4_game_mechanics as pgm


class GameMechanics(unittest.TestCase):
    def setUp(self):
        self._gamestate = pgm.GameState()
        self._faller = pgm.Faller('X', 'Y', 'Z', 2)

    '''
    These check the class functions    
    '''
    def test_intialize_field_has_size_zero(self):
        self.assertEqual(len(self._gamestate.show_field()), 0)

    def test_initialize_row_and_column_field(self):
        # random rows and columns for tests
        i = int(random.random() * 100 + 4)
        j = int(random.random() * 100 + 3)
        self._gamestate.initialize_field(i, j, 'EMPTY')
        # row
        self.assertEqual(len(self._gamestate.show_field()), i + 1)
        # column
        self.assertEqual(len((self._gamestate.show_field())[0]), j)

    def test_created_faller_with_three_jewels(self):
        self.assertIsNotNone(self._faller)
        self.assertEqual(len(self._faller.show_column_info()), 3)

    def test_rotate_faller(self):
        topF, midF, botF = self._faller.show_column_info()
        tF, mF, bF = self._faller.faller_rotating(topF, midF, botF)
        self.assertEqual(tF, 'Z')
        self.assertEqual(mF, 'X')
        self.assertEqual(bF, 'Y')

    def test_move_right_faller(self):
        col = self._faller.faller_right()
        self.assertEqual(col, 3)

    def test_move_left_faller(self):
        col = self._faller.faller_left()
        self.assertEqual(col, 1)


    '''
    These check the game functions outside of class
    '''
    def test_print_faller_object_on_board(self):
        self._gamestate.initialize_field(5, 5, 'EMPTY')
        pgm.faller_falling(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(row, 1)
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Z]')
        pgm.faller_falling(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(row, 2)
        self.assertEqual(self._gamestate.show_field()[row - 2][col - 1], '[Y]')
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Z]')
        pgm.faller_falling(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(row, 3)
        self.assertEqual(self._gamestate.show_field()[row - 3][col - 1], '[X]')
        self.assertEqual(self._gamestate.show_field()[row - 2][col - 1], '[Y]')
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Z]')

    def test_print_faller_move_right(self):
        self._gamestate.initialize_field(5, 5, 'EMPTY')
        # drop 3 rows
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        # move right
        pgm.faller_move_right(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(col, 3)
        self.assertEqual(self._gamestate.show_field()[row - 3][col - 1], '[X]')
        self.assertEqual(self._gamestate.show_field()[row - 2][col - 1], '[Y]')
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Z]')
        # moving right past border
        pgm.faller_move_right(self._faller, self._gamestate)
        pgm.faller_move_right(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(col, 5)
        pgm.faller_move_right(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertLessEqual(col, 5)
        self.assertGreaterEqual(col, 1)

    def test_print_faller_move_left(self):
        self._gamestate.initialize_field(5, 5, 'EMPTY')
        # drop 3 rows
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        # move right
        pgm.faller_move_left(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(col, 1)
        self.assertEqual(self._gamestate.show_field()[row - 3][col - 1], '[X]')
        self.assertEqual(self._gamestate.show_field()[row - 2][col - 1], '[Y]')
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Z]')
        # moving right past border
        pgm.faller_move_left(self._faller, self._gamestate)
        pgm.faller_move_left(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(col, 1)
        self.assertLessEqual(col, 5)
        self.assertGreaterEqual(col, 1)

    def test_print_faller_rotate(self):
        self._gamestate.initialize_field(5, 5, 'EMPTY')
        # drop 3 rows
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_falling(self._faller, self._gamestate)
        pgm.faller_rotate(self._faller, self._gamestate)
        row, col = self._faller.show_current_row_col()
        self.assertEqual(self._gamestate.show_field()[row - 3][col - 1], '[Z]')
        self.assertEqual(self._gamestate.show_field()[row - 2][col - 1], '[X]')
        self.assertEqual(self._gamestate.show_field()[row - 1][col - 1], '[Y]')

    # check matching
    def test_basic_match_and_clear(self):
        self._gamestate.initialize_field(5, 5, 'EMPTY')
        theFaller = pgm.Faller('X', 'X', 'X', 3)
        pgm.faller_falling(theFaller, self._gamestate)
        pgm.faller_falling(theFaller, self._gamestate)
        pgm.faller_falling(theFaller, self._gamestate)
        pgm.faller_falling(theFaller, self._gamestate)
        pgm.faller_falling(theFaller, self._gamestate)
        isMatching, hasFroze, gameOver = pgm.faller_falling(theFaller, self._gamestate)
        self.assertTrue(isMatching)
        pgm.clear_matches(theFaller, self._gamestate, 5)
        for i in range(5):
            for j in range(5):
                self.assertEqual(self._gamestate.show_field()[i][j], '   ')


if __name__ == '__main__':
    unittest.main()