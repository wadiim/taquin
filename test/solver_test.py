import unittest

from solver import Solver
from state import State, Direction


class SolverTest:
    def configure(self):
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

    def setUp(self) -> None:
        self.configure()
        self.solver = Solver()

    def test_solve_if_already_solved_then_returns_the_input_state(self):
        self.assertEqual(self.solved, self.solver.solve(self.solved, "RDLU"))

    def test_solve_if_is_not_solvable_then_raises_an_exception(self):
        state = State([
            [1, 8, 2],
            [0, 4, 3],
            [6, 7, 5]
        ])
        with self.assertRaises(Exception) as c:
            self.solver.solve(state, "RDLU")
        self.assertEqual("Not solvable", str(c.exception))

    def test_solve_if_order_length_is_not_equal_to_4_then_raises_and_exception(self):
        with self.assertRaises(Exception) as c:
            self.solver.solve(self.solved, "RL")
        self.assertEqual("Invalid search order", str(c.exception))

    def test_solve_if_directions_in_order_repeats_then_raises_an_exception(self):
        with self.assertRaises(Exception) as c:
            self.solver.solve(self.solved, "RRLU")
        self.assertEqual("Invalid search order", str(c.exception))

    def test_solve_if_one_step_from_target_state_then_returns_solved_state(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state.get_target_state(), self.solver.solve(state, "RDLU"))

    def test_solve_if_one_step_from_target_state_then_returns_state_with_correct_parent(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(state, self.solver.solve(state, "RDLU").parent)

    def test_solve_if_one_step_from_target_state_then_returns_state_with_correct_operator(self):
        state = self.solved.move(Direction.UP)
        self.assertEqual(Direction.DOWN, self.solver.solve(state, "RDLU").operator)

    def test_solve_if_unsolved_then_returns_solved_state(self):
        self.assertEqual(self.unsolved.get_target_state(), self.solver.solve(self.unsolved, "RDLU"))

    def test_solve_if_unsolved_then_the_oldest_ancestor_of_the_result_state_is_the_input_state(self):
        state = self.solver.solve(self.unsolved, "RDLU").parent
        while state.parent is not None:
            state = state.parent
        self.assertEqual(self.unsolved, state)

    def test_solve_if_unsolved_then_the_operator_chain_is_correct(self):
        operators = []
        state = self.solver.solve(self.unsolved, "RDLU")
        while state is not None and state.operator is not None:
            operators.append(state.operator)
            state = state.parent

        result = self.unsolved
        for o in reversed(operators):
            result = result.move(o)

        self.assertEqual(self.unsolved.get_target_state(), result)
