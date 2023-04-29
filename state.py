from enum import Enum


class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


class State:
    DIRECTION_TO_VECTOR_MAP = {
        Direction.LEFT: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.UP: (-1, 0),
        Direction.DOWN: (1, 0)
    }

    def __init__(self, board, parent=None, operator=None):
        values = set()
        for row in board:
            for val in row:
                if val not in values:
                    values.add(val)
                elif val == 0:
                    raise ValueError('Invalid board: Multiple blank fields')
                else:
                    raise ValueError(f'Invalid board: Value {val} occurs more than once')

            if len(row) != len(board[0]):
                raise ValueError('Invalid board: Rows have different sizes')

        # Look for missing values
        for val in range(0, len(board) * len(board[0])):
            if val not in values:
                raise ValueError(f'Invalid board: Value {val} is missing')

        self.board = tuple(map(tuple, board))
        self.parent = parent
        self.operator = operator

    def is_solvable(self):
        inv_count = self.get_inversion_count()
        length = len(self)

        if length % 2 != 0:
            return inv_count % 2 == 0
        else:
            blank_row_pos, _ = self.get_blank_position()
            if blank_row_pos % 2 != 0:
                return inv_count % 2 == 0
            else:
                return inv_count % 2 != 0

    def get_target_state(self):
        target = []
        row_length = len(self.board[0])

        for row in range(0, len(self.board)):
            target.append([])
            for col in range(0, row_length):
                target[row].append(row * row_length + (col + 1))

        target[len(target) - 1][row_length - 1] = 0
        return State(target)

    def move(self, direction: Direction):
        row, col = self.get_blank_position()
        row_shift, col_shift = self.DIRECTION_TO_VECTOR_MAP[direction]
        new_row, new_col = row + row_shift, col + col_shift
        if new_row < 0 or new_row > len(self.board) - 1 or new_col < 0 or new_col > len(self.board[row]) - 1:
            return None
        bl = [list(row) for row in self.board]
        bl[row][col], bl[new_row][new_col] = bl[new_row][new_col], bl[row][col]
        return State(bl, self, direction)

    def get_neighbours(self, order):
        neighbours = []
        for d in order:
            neighbour = self.move(Direction(d))
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    def get_inversion_count(self):
        # Flatten the board for convenience
        flattened = []
        for row in self.board:
            for val in row:
                flattened.append(val)

        inv_count = 0
        for i in range(len(flattened) - 1):
            for j in range(i + 1, len(flattened)):
                if flattened[i] and flattened[j] and flattened[i] > flattened[j]:
                    inv_count += 1

        return inv_count

    def get_blank_position(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return i, j

    def __len__(self):
        return len(self.board) * len(self.board[0])

    def __eq__(self, other):
        if isinstance(other, State):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash(self.board)
