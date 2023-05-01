from typing import Optional
import heapq

from state import State


def manhattan_distance(state: State) -> int:
    distance = 0

    for index, value in enumerate(state.board):
        if value == 0:
            continue
        goal_row = (value - 1) // state.width
        goal_col = (value - 1) % state.width
        row = index // state.width
        col = index % state.width
        distance += abs(goal_row - row) + abs(goal_col - col)

    return distance


def hamming_distance(state: State) -> int:
    distance = 0
    goal = state.get_target_state()

    for index, value in enumerate(state.board):
        if value != 0 and value != goal.board[index]:
            distance += 1

    return distance


class AStarSolver:
    @staticmethod
    def solve(state, heuristic=manhattan_distance) -> Optional[State]:
        if not state.is_solvable():
            raise Exception("Not solvable")

        goal = state.get_target_state()
        priority = heuristic(state)
        frontier = [(priority, state, 0)]
        visited = set()

        while len(frontier) > 0:
            _, node, depth = heapq.heappop(frontier)
            if node == goal:
                return node
            visited.add(node)
            for neighbour in node.get_neighbours("URDL"):
                if neighbour not in visited:
                    priority = (depth + 1) + heuristic(neighbour)
                    heapq.heappush(frontier, (priority, neighbour, depth + 1))

        return None
