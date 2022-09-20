from turtle import Vec2D
from typing import Tuple
import pygame

from pygame.surface import Surface
from Engine.image import Image

from Engine.vector import Vector


class Unit:
    position: Vector
    color: Tuple[int,int,int]
    test_img: Image
    def __init__(self, position: Vector):
        self.position = position + Vector(0,-14)
        self.color = (0,200,0)
        self.tower_img = Image('./res/sprites/tower.png')
        pass

    def draw(self, surface: Surface, offset: Vector = Vector()):
        self.tower_img.draw(
            surface,
            self.position,
            offset
        )