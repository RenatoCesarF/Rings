from __future__ import annotations

class Vector:
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def get_copy(self) -> Vector:
        return Vector(self.x, self.y)

    @property
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(tuple: tuple[int,int]) -> Vector:
        return Vector(tuple[0], tuple[1])
    
    def __str__(self):
        return f"X: {int(self.x)} Y: {int(self.y)}"

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def __eq__(self, compared: object) -> bool:
        if type(compared) == type(self):
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

