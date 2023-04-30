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
        width = len(board[0])
        height = len(board)
        seen_values = set()

        # Check for duplicated values
        for row in board:
            if len(row) != width:
                raise ValueError('Invalid board: Rows have different sizes')
            for value in row:
                if value in seen_values:
                    raise ValueError(f'Invalid board: Value {value} occurs more than once')
                seen_values.add(value)

        # Check for missing values
        values = set(range(width * height))
        if seen_values != values:
            raise ValueError(f'Invalid board: Values {values - seen_values} are missing')

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
        width = len(self.board[0])
        height = len(self.board)

        for row in range(0, height):
            target.append([])
            for col in range(0, width):
                target[row].append(row * width + (col + 1))

        target[height - 1][width - 1] = 0
        return State(target)

    def move(self, direction: Direction):
        row, col = self.get_blank_position()
        row_diff, col_diff = self.DIRECTION_TO_VECTOR_MAP[direction]
        new_row, new_col = row + row_diff, col + col_diff

        if new_row < 0 or new_col < 0 or new_row >= len(self.board) or new_col >= len(self.board[row]):
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
        flattened = [item for row in self.board for item in row]

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

    def __repr__(self):
        return f'State(parent={hex(id(self.parent)) if self.parent is not None else None}, '\
               f'operator={self.operator}, board={self.board})'
