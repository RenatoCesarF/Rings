from turtle import Vec2D
from typing import Tuple
import pygame

from pygame.surface import Surface
from Engine.image import Image

from Engine.vector import Vector
from Engine.window import Window


class Unit:
    tile_position: Vector
    screen_position: Vector
    test_img: Image
    unique_id: int
    def __init__(self, tile_position: Vector, id: int = 0):
        self.unique_id = id
        self.tile_position = tile_position
        self.screen_position = Window.to_screen(
            tile_position.x,
            tile_position.y
        ) + Vector(0,-14)
        self.color = (0,200,0)
        self.tower_img = Image('./res/sprites/tower.png')

    def draw(self, surface: Surface, offset: Vector = Vector()):
        self.tower_img.draw(
            surface,
            self.screen_position,
            offset
        )
    def __str__(self) -> str:
        return f"(id: {self.unique_id}; tile position: {self.tile_position};  "