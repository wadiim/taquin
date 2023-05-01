from typing import Optional
from collections import deque

from solver import Solver
from state import State


class BFSSolver(Solver):
    @staticmethod
    def solve(state: State, order: str) -> Optional[State]:
        Solver.solve(state, order)

        goal = state.get_target_state()

        frontier = deque([state])
        visited = set()

        while len(frontier) > 0:
            node = frontier.popleft()
            if node == goal:
                return node
            visited.add(node)
            for neighbour in node.get_neighbours(order):
                if neighbour not in visited:
                    frontier.append(neighbour)

        return None
