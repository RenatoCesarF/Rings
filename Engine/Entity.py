import pygame
from Engine.Vector import Vector
from abc import ABC


class Entity:
    position: Vector

    def __init__(self, position: Vector):
        self.position = position

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface, offset: float) -> None:
        pass
