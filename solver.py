from abc import ABC, abstractmethod
from typing import Optional

from state import State


class Solver(ABC):
    @staticmethod
    @abstractmethod
    def solve(state: State, order: str) -> Optional[State]:
        if not state.is_solvable():
            raise Exception("Not solvable")
        if len(order) != 4 or 'L' not in order or 'R' not in order or 'U' not in order or 'D' not in order:
            raise Exception("Invalid search order")

        return
