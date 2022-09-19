from turtle import Vec2D
from typing import Tuple
import pygame

from pygame.surface import Surface

from Engine.vector import Vector


class Unit:
    position: Vector
    color: Tuple[int,int,int]
    def __init__(self, position: Vector):
        self.position = position
        self.color = (0,200,0)
        pass

    def draw(self, surface: Surface):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.position.x, self.position.y, 10,10),  # type: ignore
            width=0,
            border_radius=2,
        )