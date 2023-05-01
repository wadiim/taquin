from typing import Optional

from solver import Solver
from state import State


class DFSSolver(Solver):
    @staticmethod
    def solve(state: State, order: str, max_depth=32) -> Optional[State]:
        Solver.solve(state, order)

        goal = state.get_target_state()
        if state == goal:
            return state

        stack = [(state, 0)]
        visited = set()

        while len(stack) > 0:
            node, depth = stack.pop()
            if node not in visited:
                visited.add(node)
                if node == goal:
                    return node
                if depth >= max_depth:
                    continue
                for neighbour in reversed(node.get_neighbours(order)):
                    if neighbour not in visited:
                        stack.append((neighbour, depth + 1))

        return None
