import unittest

from state import State, Direction
from a_star import AStarSolver, hamming_distance, manhattan_distance


class AStarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.solved = State([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.unsolved = State([
            [7, 5, 4],
            [0, 3, 2],
            [8, 1, 6]
        ])
        self.puzzle15 = State([
            [1, 3, 0, 4],
            [5, 2, 7, 8],
            [9, 6, 11, 12],
            [13, 10, 14, 15]
        ])

    def test_manhattan_distance_if_solved_then_returns_0(self):
        self.assertEqual(0, manhattan_distance(self.solved))

    def test_manhattan_distance_if_unsolved_then_returns_correct_distance(self):
        state = self.solved.move(Direction.LEFT).move(Direction.LEFT).move(Direction.UP)
        self.assertEqual(3, manhattan_distance(state))

    def test_hamming_distance_if_solved_then_returns_0(self):
        self.assertEqual(0, hamming_distance(self.solved))

    def test_hamming_distance_if_unsolved_then_returns_correct_distance(self):
        state = self.solved.move(Direction.LEFT).move(Direction.LEFT).move(Direction.UP)
        self.assertEqual(3, hamming_distance(state))

    def test_solve_if_already_solved_then_returns_the_input_state(self):
        self.assertEqual(self.solved, AStarSolver.solve(self.solved))

    def test_solve_if_is_not_solvable_then_raises_an_exception(self):
        state = State([
            [1, 8, 2],
            [0, 4, 3],
            [6, 7, 5]
        ])
        with self.assertRaises(Exception) as c:
            AStarSolver.solve(state)
        self.assertEqual("Not solvable", str(c.exception))

    def test_solve_if_one_step_from_target_state_then_returns_solved_state(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state.get_target_state(), AStarSolver.solve(state))

    def test_solve_if_one_step_from_target_state_then_returns_state_with_correct_parent(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state, AStarSolver.solve(state).parent)

    def test_solve_if_one_step_from_target_state_then_returns_state_with_correct_operator(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(Direction.DOWN, AStarSolver.solve(state).operator)

    def test_solve_if_unsolved_then_returns_solved_state(self):
        self.assertEqual(self.unsolved.get_target_state(), AStarSolver.solve(self.unsolved))

    def test_solve_if_unsolved_then_the_oldest_ancestor_of_the_result_state_is_the_input_state(self):
        state = AStarSolver.solve(self.unsolved).parent
        while state.parent is not None:
            state = state.parent
        self.assertEqual(self.unsolved, state)

    def test_solve_if_unsolved_then_the_operator_chain_is_correct(self):
        operators = []
        state = AStarSolver.solve(self.unsolved)
        while state is not None and state.operator is not None:
            operators.append(state.operator)
            state = state.parent

        result = self.unsolved
        for o in reversed(operators):
            result = result.move(o)

        self.assertEqual(self.unsolved.get_target_state(), result)

    def test_solve_if_hamming_heuristic_then_returns_solved_state(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state.get_target_state(), AStarSolver.solve(state, hamming_distance))

    def test_solve_if_manhattan_heuristic_then_returns_solved_state(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state.get_target_state(), AStarSolver.solve(state, manhattan_distance))

    def test_solve_if_15_puzzle_then_returns_solved_state(self):
        self.assertEqual(self.puzzle15.get_target_state(), AStarSolver.solve(self.puzzle15))

    def test_solve_if_15_puzzle_then_the_oldest_ancestor_of_the_result_state_is_the_input_state(self):
        state = AStarSolver.solve(self.puzzle15).parent
        while state.parent is not None:
            state = state.parent
        self.assertEqual(self.puzzle15, state)

    def test_solve_if_15_puzzle_then_the_operator_chain_is_correct(self):
        operators = []
        state = AStarSolver.solve(self.puzzle15)
        while state is not None and state.operator is not None:
            operators.append(state.operator)
            state = state.parent

        result = self.puzzle15
        for o in reversed(operators):
            result = result.move(o)

        self.assertEqual(self.puzzle15.get_target_state(), result)


if __name__ == '__main__':
    unittest.main()
