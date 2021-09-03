from __future__ import annotations
from typing import Tuple


class Vector():
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
    
    def add(self, vector) -> None:
        self.x += vector.x
        self.y += vector.y
        return self

    def get(self) -> Tuple:
        return (self.x, self.y)


    def __str__(self):
        return f"X: {self.x}\n Y: {self.y}"

    def __eq__(self,vector: Vector):
        self.x = vector.x
        self.y = vector.y
    
    def __add__(self,other: Vector) -> None:
        self.x += other.x
        self.y += other.y

    def __sub__(self,other: Vector) -> None:
        self.x -= other.x
        self.y -= other.y
