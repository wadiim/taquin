from typing import Optional

from solver import Solver
from state import State


class DFSSolver(Solver):
    @staticmethod
    def solve(state: State, order: str) -> Optional[State]:
        Solver.solve(state, order)

        goal = state.get_target_state()
        if state == goal:
            return state

        stack = [state]
        visited = set()

        while len(stack) > 0:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbour in reversed(node.get_neighbours(order)):
                    if neighbour == goal:
                        return neighbour
                    if neighbour not in visited:
                        stack.append(neighbour)

        return None
