"""Functions that don't have a specific folder or class yet"""

from typing import Tuple
from pygame.font import Font
from Engine.vector import Vector
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

def draw_text(font: Font, text: str, surface: Surface, position: Vector):
    interface_surface: Surface = font.render(text, False, "White")
    surface.blit(interface_surface, position.to_tuple)


def rotate(surface: pygame.Surface, angle: float, witdh: int, height: int) -> Tuple[Surface, Rect]:
    rotated_surface: Surface = pygame.transform.rotozoom(surface, angle, 1)
    rotated_rect = rotated_surface.get_rect(center=(witdh, height))
    return (rotated_surface, rotated_rect)
