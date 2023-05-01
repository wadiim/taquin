import unittest

from bfs import BFSSolver
from solver_test import SolverTest


class BFSTest(unittest.TestCase, SolverTest):
    def setUp(self) -> None:
        super().configure()
        self.solver = BFSSolver()


if __name__ == '__main__':
    unittest.main()
