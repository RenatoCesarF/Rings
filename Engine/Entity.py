from pygame import Surface
from pygame.rect import Rect
from Engine.vector import Vector
from Engine.utils import draw_collision_rect

# from utils import draw_collision_rect
# from vector import Vector


class Entity:
    position: Vector
    name: str
    collision_rect: Rect
    size: tuple

    def __init__(self, position: Vector, size: tuple, name: str = "") -> None:
        self.position = position
        self.size = size
        self.name = name
        # self.collision_rect = Rect(self.position.as_tuple, (self.size[0], self.size[1]))

    def update(self) -> None:
        """Update function"""

    def draw(self, surface: Surface, offset: Vector = Vector()) -> None:
        # draw_collision_rect(self.collision_rect, surface, offset, line_width=0)
        pass

    def __str__(self) -> str:
        return f"Entity(name: {self.name}, position: {self.position}"
