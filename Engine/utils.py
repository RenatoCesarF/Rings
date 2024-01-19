"""Functions that don't have a specific folder or class yet"""

from typing import Tuple
from pygame.font import Font
from Engine.Vector import Vector
import pygame
from pygame.surface import Surface
from pygame.rect import Rect


def draw_text(font: Font, text: str, surface: Surface, position: Vector):
    interface_surface: Surface = font.render(text, False, "White")
    surface.blit(interface_surface, position.as_tuple)


def rotate(
    surface: pygame.Surface, angle: float, witdh: int, height: int
) -> Tuple[Surface, Rect]:
    rotated_surface: Surface = pygame.transform.rotozoom(surface, angle, 1)
    rotated_rect = rotated_surface.get_rect(center=(witdh, height))
    return (rotated_surface, rotated_rect)


def draw_collision_rect(
    collision_rect: pygame.Rect, surface: Surface, offset: Vector, line_width: int = 1
):
    pygame.draw.rect(
        surface,
        (100, 0, 0),
        pygame.Rect(
            collision_rect.x - offset.x,  # +left_offset.x,
            collision_rect.y - offset.y,  # +left_offset.y,
            collision_rect.width,
            collision_rect.height,
        ),
        width=line_width,
    )


def draw_circle(
    destination: Surface, position: list, radius: int, color: Tuple, offset: Vector
):
    shape_surf = pygame.Surface((radius, radius), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, position, radius)

    shape_surf.set_alpha(color[3])
    destination.blit(
        shape_surf,
        pygame.Rect(position[0] - offset.x, position[1] - offset.y, radius, radius),
    )
