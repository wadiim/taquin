import timeit


def bench(snippet, number=1_000_000, repeat=5, setup=''):
    return timeit.repeat(
        snippet,
        number=number,
        repeat=repeat,
        setup=setup
    )


if __name__ == '__main__':
    setup = 'from state import State, Direction; '\
            'state = State([[13, 2, 10, 3], [1, 12, 8, 4], [5, 0, 9, 6], [15, 14, 11, 7]])'
    snippets = [
        'state.get_blank_position()',
        'state.get_inversion_count()',
        'state.is_solvable()',
        'state.get_target_state()',
        'state.get_neighbours("URDL")',
        'state.move(Direction.RIGHT)'
    ]

    for s in snippets:
        print(f'{s}: {round(min(bench(s, setup=setup)), 2)}')
