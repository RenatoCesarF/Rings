import pygame
from Engine.Vector import Vector


class Tile:
    position: Vector
    size: int
    color: tuple
    thikness: int
    content: int 

    def __init__(self, position: Vector, size: int, content: int = 0, thikness: int = 0):
        self.content = content or 0
        self.position = position
        self.size = size
        self.color = self.get_tile_color_by_index(self.content)
        self.thikness = thikness

    def draw(self, surface: pygame.Surface, offset: Vector):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(
                self.position.x - offset.x,
                self.position.y - offset.y,
                self.size,
                self.size,
            ),
                width=self.thikness
        )

    def get_tile_color_by_index(self, index: int):
        if index == 1:
            return (90, 90, 90)
        elif index == 2:
            return (190, 90, 90)
        elif index == 3:
            return (90, 190, 90)
        elif index == 4:
            return (30,30,30)
        elif index == 6:
            return (0,200,0)
        else:
            return (90, 190, 90)
        
    def __str__(self) -> str:
        return f"( {self.position} , {self.size} , {self.color} , {self.thikness}"
