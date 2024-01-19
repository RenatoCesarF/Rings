from __future__ import annotations

from Engine.Vector import Vector


class CollisionRect:
    position: Vector
    width: int
    height: int

    def __init__(self, position: Vector, width: int, height: int):
        self.position = position
        self.width = width
        self.height = height

    def is_colliding_with(self, rect: CollisionRect) -> bool:
        return False
        pass

    def is_point_colliding(self, point: Vector) -> bool:
        return False
        pass
