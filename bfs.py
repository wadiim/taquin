from typing import Optional, Tuple
from collections import deque

from solver import Solver
from state import State


class BFSSolver(Solver):
    @staticmethod
    def solve(state: State, order: str) -> Tuple[Optional[State], int, int, int]:
        Solver.solve(state, order)

        goal = state.get_target_state()

        frontier = deque([(state, 0)])
        explored = set()
        num_of_visited = 1
        max_depth = 0

        while len(frontier) > 0:
            node, depth = frontier.popleft()
            explored.add(node)
            if node == goal:
                return node, num_of_visited, len(explored), max_depth
            for neighbour in node.get_neighbours(order):
                if neighbour not in explored:
                    frontier.append((neighbour, depth + 1))
                    num_of_visited += 1
                    if depth + 1 > max_depth:
                        max_depth = depth + 1

        return None, num_of_visited, len(explored), max_depth
