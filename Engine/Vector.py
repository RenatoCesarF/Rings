from __future__ import annotations
import math


class Vector:
    """Representation of a position or a movement"""

    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    @staticmethod
    def from_tuple(tp: tuple[int, int]) -> Vector:
        return Vector(tp[0], tp[1])

    @staticmethod
    def zero() -> Vector:
        return Vector(0, 0)

    def is_equal(self, vector: Vector) -> bool:
        if isinstance(self, Vector):
            return False

        return self.x == vector.x and self.y == vector.y

    def normalize(self) -> Vector:
        normal_vector = self.x * self.x + self.y * self.y
        if normal_vector == 0:
            return Vector(0, 0)
        normal_vector = math.sqrt(normal_vector)
        return Vector(int(self.x / normal_vector), int(self.y / normal_vector))

    def divided_by_number(self, number: int) -> Vector:
        if number == 0:
            return Vector(0, 0)
        return Vector(int(self.x / number), int(self.y / number))

    def divided_by_vector(self, vector: Vector) -> Vector:
        return Vector(int(self.x / vector.x), int(self.y / vector.y))

    def __str__(self):
        return f'Vector(x: {int(self.x)}, y: {int(self.y)})'

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def __eq__(self, compared: object) -> bool:
        if not isinstance(compared, Vector):
            return False

        return self.x == compared.x and self.y == compared.y  # type: ignore

    def __add__(self, other: Vector):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vector):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def __truediv__(self, other: Vector):
        self.x = int(self.x / other.x)
        self.y = int(self.y / other.y)
        return self
