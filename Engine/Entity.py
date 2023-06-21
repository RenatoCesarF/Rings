import pygame
from Engine.vector import Vector


class Entity:
    position: Vector
    name: str

    def __init__(self, position: Vector, name: str = None) -> None:
        self.position = position
        self.name = name

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface, offset: Vector = Vector()) -> None:
        pass

    def __str__(self) -> str:
        return f"Entity(name: {self.name}, position: {self.position}"
