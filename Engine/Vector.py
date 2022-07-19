from __future__ import annotations
from typing import Tuple


class Vector:
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def get(self) -> Vector:
        return Vector(self.x, self.y)

    def __str__(self):
        return f"X: {self.x} Y: {self.y}"

    def __eq__(self, vector: Vector):
        self.x = vector.x
        self.y = vector.y

    def __add__(self, other: Vector):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vector):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self
    
    def __truediv__(self,other: Vector):
        self.x = self.x / other.x
        self.y = self.y / other.y
        return self

