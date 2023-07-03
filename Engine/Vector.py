from __future__ import annotations
import math


class Vector:
    """Representation of a position or a movement"""
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


    @property
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    @staticmethod
    def from_tuple(tuple: tuple[int, int]) -> Vector:
        return Vector(tuple[0], tuple[1])

    def is_equal(self, vector: Vector) -> bool:
        if type(vector) != type(self):
            return False

        return (self.x == vector.x and self.y == vector.y)

    def normalize(self) -> Vector():
        l = self.x * self.x + self.y * self.y
        if l == 0:
            return Vector(0, 0)
        l = math.sqrt(l)
        return Vector(self.x / l, self.y / l)

    def divided_by_number(self, number: int) -> Vector:
        if number == 0:
            return Vector(0, 0)
        return Vector(int(self.x / number), int(self.y / number))

    def divided_by_vector(self, vector: Vector) -> Vector:
        return Vector(int(self.x / vector.x), int(self.y / vector.y))
        

    def __str__(self):
        return f"Vector(x: {int(self.x)}, y: {int(self.y)})"

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def __eq__(self, compared: object) -> bool:
        if type(compared) != type(self):
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
