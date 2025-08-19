from Engine.Window import Window
import pygame

from Engine.Entity import Entity
from Engine.Vector import Vector
from Engine.image import Image
from Engine.utils import draw_collision_rect

class Enemy:
    position: Vector
    collision_rect: pygame.Rect
    life: int
    speed: int
    width: int
    height: int
    image: Image

    def __init__(self, position: Vector, width: int, height: int):
        self.img = Image('./res/sprites/tower.png', (255, 0, 0))
        self.position = position
        self.screen_position = Window.to_isometric_position_from_vector(position)

        self.width = width
        self.height = height
        self.collision_rect = pygame.Rect(
            self.position.x, self.position.y, width, height
        )

    def draw(self, surface: pygame.Surface, offset: Vector = Vector.zero()):
        pos = Window.to_isometric_position_from_vector(self.position) 
        # pos = Window.to_isometric_position_non_tile(self.position.x, self.position.y)

        pygame.draw.circle(
            surface,
            (255, 0, 0),
            ( pos.x, pos.y),
            5,
            0,
        )

    def update(self):
        pass

        # self.collision_rect.x = self.position.x
        # self.collision_rect.y = self.position.y

