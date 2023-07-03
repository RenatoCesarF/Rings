from pygame import Surface
from pygame.rect import Rect
from Engine.vector import Vector

class Entity: 
    """The base Entity class"""
    position: Vector
    name: str

    collision_rect: Rect


    def __init__(self, position: Vector, name: str = "") -> None:
        self.position = position
        self.name = name

    def update(self) -> None:
        """Update function"""

    def draw(self, surface: Surface, offset: Vector = Vector()) -> None:
        """Draw function"""

    def __str__(self) -> str:
        return f"Entity(name: {self.name}, position: {self.position}"


