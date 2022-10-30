from typing import Tuple
from pygame import Surface
import pygame

from Engine.vector import Vector


class Image:
    surface: Surface
    color_key: Tuple[int,int,int]
    width   : int
    height: int
    def __init__(self, directory: str, color_key: Tuple[int,int,int] = (0,0,0), scale: float = 1):
        self.surface: Surface = pygame.image.load(directory).convert()
        self.surface.set_colorkey(color_key)
        
        self.color_key = color_key
        self.width  = self.surface.get_width() * scale
        self.height = self.surface.get_height() * scale
        
        if scale == 1:
            return
        # separate this bollow into functino
        self.surface = pygame.transform.scale(
            self.surface,
            (int(self.width), int(self.height))
        )

    
    def set_opacity(self, opacity_alpha: int):
        self.surface.set_alpha(opacity_alpha)
        
    def draw_outline(self, surface: Surface, position: Vector, offset: Vector):
        mask_outline = pygame.mask.from_surface(self.surface).to_surface()
        mask_outline.set_colorkey((0, 0, 0))
        loc = (position.x - offset.x, position.y - offset.y)
        surface.blit(mask_outline, (loc[0]-1, loc[1]))
        surface.blit(mask_outline, (loc[0]+1, loc[1]))
        surface.blit(mask_outline, (loc[0], loc[1]-1))
        surface.blit(mask_outline, (loc[0], loc[1]+1))

    def get_mask(self) -> Surface:
        mask = (
            pygame.mask
            .from_surface(self.surface)
            # .to_surface()
        )
        # mask.set_colorkey((0,0,0))
        return mask
        
    def draw(self, surface: Surface, position: Vector, offset: Vector):
        surface.blit(
            self.surface,
            (position.x - offset.x, position.y - offset.y),
        )