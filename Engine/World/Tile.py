from typing import Tuple
import pygame
from Engine.Vector import Vector


class Tile:
    position: Vector
    size: int
    grid_index: Vector
    color: Tuple[int, int, int]
    thikness: int
    content: int

    def __init__(
        self,
        position: Vector,
        size: int,
        grid_index: Vector = Vector.zero(),
        content: int = 0,
        color: Tuple[int, int, int] = (100, 100, 100),
        thikness: int = 0,
    ):
        self.content = content or 0
        self.grid_index = grid_index
        self.position = position
        self.size = size
        self.color = color
        self.thikness = thikness

    def draw(self, surface: pygame.Surface, offset: Vector = Vector.zero()):
        pygame.draw.rect(
            surface,
            self.get_tile_color_by_index(self.content),
            pygame.Rect(
                self.position.x - offset.x,
                self.position.y - offset.y,
                self.size,
                self.size,
            ),
            width=self.thikness,
        )

    @staticmethod
    def get_tile_color_by_index(index: int):
        if index == 0:
            return (0, 0, 0)
        elif index == 1:
            return (90, 90, 90)
        elif index == 2:
            return (190, 90, 90)
        elif index == 3:
            return (90, 190, 90)
        elif index == 4:
            return (30, 30, 30)
        elif index == 6:
            return (0, 200, 0)
        else:
            return (90, 190, 90)

    def __str__(self) -> str:
        return f"( Position: {self.position}, Tile Index: {self.grid_index}, Color: {self.color} , {self.thikness}"
