from typing import Tuple
from pygame import Surface
import pygame

from Engine.vector import Vector


class Image:
    surface: Surface
    def __init__(self, directory: str, color_key: Tuple[int,int,int] = (0,0,0), scale: float = 1):
        self.surface: Surface = pygame.image.load(directory).convert()
        self.surface.set_colorkey(color_key)
        
        if scale == 1:
            return
        self.surface = pygame.transform.scale(
            self.surface,
            (
                int(self.surface.get_width()*scale), 
                int(self.surface.get_height()*scale)
            )
        )
    
    def set_opacity(self, opacity_alpha: int):
        self.surface.set_alpha(opacity_alpha)
        
    def draw(self, surface: Surface, position: Vector, offset: Vector):
        surface.blit(
            self.surface,
            (position.x - offset.x, position.y - offset.y),
        )