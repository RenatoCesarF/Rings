from turtle import Vec2D
from typing import Tuple
import pygame

from pygame.surface import Surface
from pygame.rect import Rect
from Engine.entity import Entity
from Engine.image import Image
from Engine.utils import draw_collision_rect

from Engine.vector import Vector
from Engine.window import Window


class Unit(Entity):
    tile_position: Vector
    screen_position: Vector
    tower_img: Image# go to resource instance
    unique_id: int
    collision_rect: Rect #go to resource instance
    bullet_position: Vector
    def __init__(self, tile_position: Vector, id: int = 0):
        self.unique_id = id
        self.tile_position = tile_position
        
        self.screen_position = Window.to_isometric_position_from_vector(tile_position) 
        self.screen_position += Vector(0,-14)
        self.collision_rect = pygame.Rect(
             self.screen_position.x +6, self.screen_position.y,  17,27
        )
        
        self.tower_img = Image('./res/sprites/tower.png', (255,0,0))
        center_position = Vector(
            self.screen_position.x + self.tower_img.width /2,
            self.screen_position.y + self.tower_img.height /2
        )
        super().__init__(
            center_position
        )
        
    def draw(self, surface: Surface, offset: Vector = Vector()):
        self.tower_img.draw(
            surface,
            self.screen_position,
            offset
        )
        # draw_collision_rect(self.collision_rect, surface, offset)
        
    def __eq__(self, compared: object) -> bool:
        if type(compared) != type(self):
            return False
        return self.tile_position == compared.tile_position
         

    def __str__(self) -> str:
        return f"(id: {self.unique_id}; tile position: {self.tile_position};  "