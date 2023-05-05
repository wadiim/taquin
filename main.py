import sys
from timeit import default_timer as timer

from state import State
from bfs import BFSSolver
from dfs import DFSSolver
from a_star import AStarSolver, hamming_distance, manhattan_distance


def read_puzzle_file(filename) -> State:
    with open(filename, 'r') as file:
        _, height = map(int, file.readline().strip().split())  # Ignore width
        puzzle = []
        for i in range(height):
            puzzle.append(list(map(int, file.readline().strip().split())))

        return State(puzzle)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        exit(1)

    strategy = sys.argv[1]
    strategy_param = sys.argv[2]
    puzzle_file = sys.argv[3]
    solution_file = sys.argv[4]
    stats_file = sys.argv[5]

    solver = None
    if strategy == 'bfs':
        solver = BFSSolver
    elif strategy == 'dfs':
        solver = DFSSolver
    else:
        solver = AStarSolver

    param = None
    if strategy_param == 'hamm':
        param = hamming_distance
    elif strategy_param == 'manh':
        param = manhattan_distance
    else:
        param = strategy_param

    try:
        state = read_puzzle_file(puzzle_file)
        start = timer()
        solved, num_of_visited, num_of_explored, max_depth = solver.solve(state, param)
        end = timer()
        exec_time = end - start
    except Exception:
        solved = None
        num_of_visited = 0
        num_of_explored = 0
        max_depth = 0
        exec_time = 0

    solution_output = '-1'
    solution = []
    if solved is not None:
        while solved.parent is not None:
            solution.append(solved.operator.value)
            solved = solved.parent

        solution_output = str(len(solution)) + '\n' + ''.join(reversed(solution))
    with open(solution_file, 'w') as file:
        file.write(solution_output)

    with open(stats_file, 'w') as file:
        file.write((str(len(solution)) if solved is not None else '-1')
                   + f'\n{num_of_visited}\n{num_of_explored}\n{max_depth}\n'
                   + '%.3f' % (exec_time * 1000))
