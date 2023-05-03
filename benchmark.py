import timeit


def bench(snippet, number=1_000_000, repeat=5, setup=''):
    return timeit.repeat(
        snippet,
        number=number,
        repeat=repeat,
        setup=setup
    )


if __name__ == '__main__':
    state_setup = 'from state import State, Direction; from dfs import DFSSolver;' \
                  'state = State([[13, 2, 10, 3], [1, 12, 8, 4], [5, 0, 9, 6], [15, 14, 11, 7]])'
    state_snippets = [
        'state.get_blank_position()',
        'state.get_inversion_count()',
        'state.is_solvable()',
        'state.get_target_state()',
        'state.get_neighbours("URDL")',
        'state.move(Direction.RIGHT)'
    ]

    print('--- State (1 000 000 runs) ---')
    for s in state_snippets:
        print(f'{s}: {round(min(bench(s, setup=state_setup)), 2)} s')

    dfs_setup = 'from state import State, Direction; from dfs import DFSSolver;' \
                'state = State([[1, 3, 0, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]])'
    dfs_snippets = [
        'DFSSolver.solve(state, "RDUL", 20)',
        'DFSSolver.solve(state, "RDLU", 20)',
        'DFSSolver.solve(state, "DRUL", 20)',
        'DFSSolver.solve(state, "DRLU", 20)',
        'DFSSolver.solve(state, "LUDR", 20)',
        'DFSSolver.solve(state, "LURD", 20)',
        'DFSSolver.solve(state, "ULDR", 20)',
        'DFSSolver.solve(state, "ULRD", 20)'
    ]

    print('\n--- DFS (1 000 runs) ---')
    for s in dfs_snippets:
        print(f'{s}: {round(min(bench(s, number=1000, setup=dfs_setup)), 2)} s')

    bfs_setup = 'from state import State, Direction; from bfs import BFSSolver;' \
                'state = State([[1, 3, 0, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]])'
    bfs_snippets = [
        'BFSSolver.solve(state, "RDUL")',
        'BFSSolver.solve(state, "RDLU")',
        'BFSSolver.solve(state, "DRUL")',
        'BFSSolver.solve(state, "DRLU")',
        'BFSSolver.solve(state, "LUDR")',
        'BFSSolver.solve(state, "LURD")',
        'BFSSolver.solve(state, "ULDR")',
        'BFSSolver.solve(state, "ULRD")'
    ]

    print('\n--- BFS (1 000 runs) ---')
    for s in bfs_snippets:
        print(f'{s}: {round(min(bench(s, number=1000, setup=bfs_setup)), 2)} s')

    a_star_setup = 'from state import State, Direction;' \
                   'from a_star import AStarSolver, hamming_distance, manhattan_distance;' \
                   'state = State([[1, 3, 0, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]])'
    a_star_snippets = [
        'AStarSolver.solve(state, hamming_distance)',
        'AStarSolver.solve(state, manhattan_distance)'
    ]

    print('\n--- A* (1 000 runs) ---')
    for s in a_star_snippets:
        print(f'{s}: {round(min(bench(s, number=1000, setup=a_star_setup)), 2)} s')
