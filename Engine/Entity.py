import pygame
from Engine.vector import Vector

class Entity:
    position: Vector

    def __init__(self, position: Vector) -> None:
        self.position = position

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface, offset: Vector = Vector()) -> None:
        pass
