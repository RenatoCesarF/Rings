"""Functions that don't have a specific folder or class yet"""

from Engine.Vector import Vector
import pygame


def draw_text(font,text,surface, position):
    interface_surface = font.render(text, False, "White")
    surface.blit(interface_surface,position)

def rotate(surface,angle,witdh, height):
    rotated_surface = pygame.transform.rotozoom(surface,angle,1)
    rotated_rect = rotated_surface.get_rect(center =(witdh, height))
    return rotated_surface,rotated_rect

# def fill_game_map(game_map,surface: pygame.Surface, TILE_SIZE: int, camera: Vector):
  