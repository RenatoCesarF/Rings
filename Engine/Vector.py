
from typing import Tuple


class Vector2D():
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
    
    def add(self, vector) -> None:
        self.x += vector.x
        self.y += vector.y
        return self

    def to_tuple(self) -> Tuple:
        return (self.position.x, self.position.y)
