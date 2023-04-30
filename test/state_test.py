import unittest

from state import State, Direction


class StateTest(unittest.TestCase):
    def test_init_if_non_iterable_argument_passed_then_raises_type_error(self):
        self.assertRaises(TypeError, lambda: State(2))

    def test_init_if_iterable_argument_with_non_iterable_elements_passed_then_raises_type_error(self):
        self.assertRaises(TypeError, lambda: State([1, 2, 3, 0]))

    def test_init_if_board_has_rows_of_different_lengths_then_raises_value_error(self):
        board = [
            [1, 2, 3, 4],
            [5, 6],
            [7, 8, 0]
        ]
        with self.assertRaises(ValueError) as c:
            State(board)
        self.assertEqual('Invalid board: Rows have different sizes', str(c.exception))

    def test_init_if_multiple_blanks_then_raises_value_error(self):
        board = [
            [0, 1, 2],
            [3, 0, 4],
            [5, 6, 0]
        ]
        with self.assertRaises(ValueError) as c:
            State(board)
        self.assertEqual('Invalid board: Value 0 occurs more than once', str(c.exception))

    def test_init_if_repeated_values_then_raises_value_error(self):
        board = [
            [1, 2, 2],
            [3, 4, 5],
            [6, 7, 0]
        ]
        with self.assertRaises(ValueError) as c:
            State(board)
        self.assertEqual('Invalid board: Value 2 occurs more than once', str(c.exception))

    def test_init_if_number_is_missing_then_raises_value_error(self):
        board = [
            [1, 3, 4],
            [5, 6, 7],
            [8, 9, 0]
        ]
        with self.assertRaises(ValueError) as c:
            State(board)
        self.assertEqual('Invalid board: Values {2} are missing', str(c.exception))

    def test_init_if_multiple_numbers_are_missing_then_raises_value_error(self):
        board = [
            [1, 3, 5],
            [6, 7, 9],
            [10, 11, 0]
        ]
        with self.assertRaises(ValueError) as c:
            State(board)
        self.assertEqual(f'Invalid board: Values { {2, 4, 8} } are missing', str(c.exception))

    def test_init_if_called_explicitly_then_parent_is_none(self):
        state = State([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.assertIsNone(state.parent)

    def test_init_if_called_explicitly_then_operator_is_none(self):
        state = State([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.assertIsNone(state.operator)

    def test_get_inversion_count_if_no_inversions_then_returns_zero(self):
        state = State([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.assertEqual(0, state.get_inversion_count())

    def test_get_inversion_count_if_single_inversion_then_returns_one(self):
        state = State([
            [2, 1, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.assertEqual(1, state.get_inversion_count())

    def test_get_inversion_count_if_multiple_inversions_then_returns_correct_number(self):
        state = State([
            [1, 8, 2],
            [0, 4, 3],
            [7, 6, 5]
        ])
        self.assertEqual(10, state.get_inversion_count())

    def test_is_solvable_if_already_solved_then_returns_true(self):
        state = State([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.assertTrue(state.is_solvable())

    def test_is_solvable_if_odd_number_of_fields_and_odd_number_of_inversions_then_returns_false(self):
        state = State([
            [1, 8, 2],
            [0, 4, 3],
            [6, 7, 5]
        ])
        self.assertFalse(state.is_solvable())

    def test_is_solvable_if_odd_number_of_fields_and_even_number_of_inversions_then_returns_true(self):
        state = State([
            [1, 8, 2],
            [0, 4, 3],
            [7, 6, 5]
        ])
        self.assertTrue(state.is_solvable())

    def test_is_solvable_if_even_number_of_fields_and_odd_number_of_inversions_and_blank_on_even_row_then_returns_true(self):
        state = State([
            [13, 2, 10, 3],
            [1, 12, 8, 4],
            [5, 0, 9, 6],
            [15, 14, 11, 7]
        ])
        self.assertTrue(state.is_solvable())

    def test_is_solvable_if_even_number_of_fields_and_even_number_of_inversions_and_blank_on_odd_row_then_returns_true(self):
        state = State([
            [6, 13, 7, 10],
            [8, 9, 11, 0],
            [15, 2, 12, 5],
            [14, 3, 1, 4]
        ])
        self.assertTrue(state.is_solvable())

    def test_is_solvable_if_even_number_of_fields_and_even_number_of_inversions_and_blank_on_even_row_then_returns_false(self):
        state = State([
            [3, 9, 1, 15],
            [14, 11, 4, 6],
            [13, 0, 10, 12],
            [2, 7, 8, 5]
        ])
        self.assertFalse(state.is_solvable())

    def test_is_solvable_if_even_number_of_fields_and_odd_number_of_inversions_and_blank_on_odd_row_then_returns_false(self):
        state = State([
            [13, 2, 10, 3],
            [1, 12, 8, 4],
            [5, 9, 6, 15],
            [0, 14, 11, 7]
        ])
        self.assertFalse(state.is_solvable())

    def test_get_target_state_if_board_has_single_field_then_returns_the_current_state(self):
        state = State([[0]])
        self.assertEqual(State([[0]]), state.get_target_state())

    def test_get_target_state_if_board_has_multiple_fields_then_returns_solved_board(self):
        state = State([
            [6, 13, 7, 10],
            [8, 9, 11, 0],
            [15, 2, 12, 5],
            [14, 3, 1, 4]
        ])
        expected = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertEqual(State(expected), state.get_target_state())

    def test_hash_if_equal_states_then_the_hashes_are_also_equal(self):
        state1 = State([
            [1, 2],
            [3, 0]
        ])
        state2 = State([
            [1, 2],
            [3, 0]
        ])
        self.assertEqual(state1, state2)
        self.assertEqual(hash(state1), hash(state2))

    def test_up_if_valid_move_then_returns_new_state(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        expected = State([
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 7, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(expected, state.move(Direction.UP))

    def test_up_if_invalid_move_then_returns_none(self):
        state = State([
            [1, 0, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertIsNone(state.move(Direction.UP))

    def test_down_if_valid_move_then_return_new_state(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 0, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        expected = State([
            [1, 2, 3, 4],
            [5, 6, 10, 7],
            [8, 9, 0, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(expected, state.move(Direction.DOWN))

    def test_down_if_invalid_move_then_returns_none(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ])
        self.assertIsNone(state.move(Direction.DOWN))

    def test_left_if_valid_move_then_return_new_state(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 0, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        expected = State([
            [1, 2, 3, 4],
            [5, 0, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(expected, state.move(Direction.LEFT))

    def test_left_if_invalid_move_then_returns_none(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [0, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertIsNone(state.move(Direction.LEFT))

    def test_right_if_valid_move_then_return_new_state(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 0, 10, 11],
            [12, 13, 14, 15]
        ])
        expected = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(expected, state.move(Direction.RIGHT))

    def test_right_if_invalid_move_then_returns_none(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertIsNone(state.move(Direction.RIGHT))

    def test_move_if_valid_then_parent_is_not_none(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        self.assertIsNotNone(state.move(Direction.UP).parent)

    def test_move_if_valid_then_parent_is_the_state_before_move(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 0, 10, 11],
            [12, 13, 14, 15]
        ])
        result = state.move(Direction.RIGHT)
        self.assertEqual(state, result.parent)

    def test_move_if_valid_then_operator_is_not_none(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 0, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertIsNotNone(state.move(Direction.DOWN).operator)

    def test_move_if_valid_then_operator_is_the_used_one(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 0, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(Direction.LEFT, state.move(Direction.LEFT).operator)

    def test_get_neighbours_if_not_an_edge_cell_then_return_correct_number_of_states(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(4, len(state.get_neighbours("RDLU")))

    def test_get_neighbours_if_not_an_edge_cell_then_returns_correct_states(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        neighbours = state.get_neighbours("RDLU")
        for d in Direction:
            self.assertIn(state.move(d), neighbours)

    def test_get_neighbours_if_not_an_edge_cell_then_returns_states_in_correct_order(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 11],
            [12, 13, 14, 15]
        ])
        order = "RDLU"
        neighbours = state.get_neighbours(order)
        i = 0
        for d in order:
            self.assertEqual(state.move(Direction(d)), neighbours[i])
            i += 1

    def test_get_neighbours_if_an_edge_cell_then_returns_correct_number_of_states(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(3, len(state.get_neighbours("RDLU")))

    def test_get_neighbours_if_an_edge_cell_then_returns_correct_states(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        neighbours = state.get_neighbours("RDLU")
        for d in (Direction.UP, Direction.LEFT, Direction.DOWN):
            self.assertIn(state.move(d), neighbours)

    def test_get_neighbours_if_an_edge_cell_then_returns_states_in_correct_order(self):
        state = State([
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        neighbours = state.get_neighbours("RDLU")
        i = 0
        for d in "DLU":
            self.assertEqual(state.move(Direction(d)), neighbours[i])
            i += 1

    def test_get_neighbours_if_a_corner_cell_then_returns_correct_number_of_states(self):
        state = State([
            [1, 2, 3, 0],
            [5, 6, 7, 4],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        self.assertEqual(2, len(state.get_neighbours("RDLU")))

    def test_get_neighbours_if_a_corner_cell_then_returns_correct_states(self):
        state = State([
            [1, 2, 3, 0],
            [5, 6, 7, 4],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        neighbours = state.get_neighbours("RDLU")
        for d in (Direction.LEFT, Direction.DOWN):
            self.assertIn(state.move(d), neighbours)

    def test_get_neighbours_if_a_corner_state_then_returns_states_in_correct_order(self):
        state = State([
            [1, 2, 3, 0],
            [5, 6, 7, 4],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])
        neighbours = state.get_neighbours("RDLU")
        i = 0
        for d in "DL":
            self.assertEqual(state.move(Direction(d)), neighbours[i])
            i += 1


if __name__ == '__main__':
    unittest.main()
