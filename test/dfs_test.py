import unittest

from dfs import DFSSolver
from solver_test import SolverTest


class DFSTest(unittest.TestCase, SolverTest):
    def setUp(self) -> None:
        super().configure()
        self.solver = DFSSolver()


if __name__ == '__main__':
    unittest.main()
