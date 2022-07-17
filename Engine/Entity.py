import pygame
from Engine.Vector import Vector
from abc import ABC

class Entity(ABC):
    position: Vector
    def update(self) -> None:
        pass
    def draw(self, surface: pygame.Surface, offset: float) -> None:
        pass

