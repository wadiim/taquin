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
        self.width = len(board[0])
        self.height = len(board)

        # Check for duplicated values
        seen_values = set()
        for row in board:
            if len(row) != self.width:
                raise ValueError('Invalid board: Rows have different sizes')
            for value in row:
                if value in seen_values:
                    raise ValueError(f'Invalid board: Value {value} occurs more than once')
                seen_values.add(value)

        # Check for missing values
        values = set(range(self.width * self.height))
        if seen_values != values:
            raise ValueError(f'Invalid board: Values {values - seen_values} are missing')

        self.board = tuple([item for row in board for item in row])
        self.parent = parent
        self.operator = operator
        self.blank_position = None

    def is_solvable(self):
        inv_count = self.get_inversion_count()

        if len(self) % 2 != 0:
            return inv_count % 2 == 0
        else:
            blank_row_pos = self.get_blank_position() // self.width
            if blank_row_pos % 2 != 0:
                return inv_count % 2 == 0
            else:
                return inv_count % 2 != 0

    def get_target_state(self):
        target = State.__new__(State)
        target.parent = None
        target.operator = None
        target.width = self.width
        target.height = self.height
        target.blank_position = len(self) - 1
        target.board = tuple([i for i in range(1, len(self))] + [0])
        return target

    def move(self, direction: Direction):
        index = self.get_blank_position()
        row_diff, col_diff = self.DIRECTION_TO_VECTOR_MAP[direction]
        row, col = index // self.width, index % self.width
        new_row, new_col = row + row_diff, col + col_diff

        if new_row < 0 or new_col < 0 or new_row >= self.height or new_col >= self.width:
            return None

        board = list(self.board)
        new_index = new_row * self.width + new_col
        board[index], board[new_index] = board[new_index], board[index]

        new_state = State.__new__(State)
        new_state.parent = self
        new_state.operator = direction
        new_state.width = self.width
        new_state.height = self.height
        new_state.blank_position = new_row * self.width + new_col
        new_state.board = tuple(board)
        return new_state

    def get_neighbours(self, order):
        neighbours = []
        for d in order:
            neighbour = self.move(Direction(d))
            if neighbour is not None:
                neighbours.append(neighbour)
        return neighbours

    def get_inversion_count(self):
        # Converting a tuple to a list noticeably improves performance for some reason
        board = list(self.board)

        inv_count = 0
        for i in range(len(self) - 1):
            for j in range(i + 1, len(self)):
                if board[i] and board[j] and board[i] > board[j]:
                    inv_count += 1

        return inv_count

    def get_blank_position(self):
        return self.board.index(0) if self.blank_position is None else self.blank_position

    def __len__(self):
        return len(self.board)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash(self.board)

    def __repr__(self):
        return f'State(parent={hex(id(self.parent)) if self.parent is not None else None}, '\
               f'operator={self.operator}, board={self.board})'
