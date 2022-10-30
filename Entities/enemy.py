import pygame

from Engine.entity import Entity
from Engine.vector import Vector
from Engine.image import Image
from Engine.utils import draw_collision_rect

class Enemy(Entity):
    position: Vector
    collision_rect: pygame.Rect
    life: int
    speed: int
    width: int
    height: int
    image: Image
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height
        self.collision_rect = pygame.Rect(
            self.position.x,
            self.position.y,
            width, height
        )

    def draw(self, surface: pygame.Surface, offset: Vector):
        draw_collision_rect(self.collision_rect, surface, offset)

    def __str__(self) -> str:
        return f"Enemy(position: {self.position}, width: {self.width}, height: {self.height})"