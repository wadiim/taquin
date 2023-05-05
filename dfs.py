from typing import Optional, Tuple

from solver import Solver
from state import State


class DFSSolver(Solver):
    @staticmethod
    def solve(state: State, order: str, depth_limit=20) -> Tuple[Optional[State], int, int, int]:
        Solver.solve(state, order)

        goal = state.get_target_state()
        stack = [(state, 0)]
        explored = set()
        node_to_depth_map = dict()
        num_of_visited = 1
        max_depth = 0

        while len(stack) > 0:
            node, depth = stack.pop()

            if node in explored and node_to_depth_map[node] > depth:
                explored.remove(node)

            if node not in explored:
                if node == goal:
                    return node, num_of_visited, len(explored), max_depth
                if depth >= depth_limit:
                    continue

                explored.add(node)
                node_to_depth_map[node] = depth

                for neighbour in reversed(node.get_neighbours(order)):
                    if neighbour not in explored:
                        num_of_visited += 1

                    stack.append((neighbour, depth + 1))
                    if depth + 1 > max_depth:
                        max_depth = depth + 1

        return None, num_of_visited, len(explored), max_depth
