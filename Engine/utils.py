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

def fill_game_map(game_map,surface: pygame.Surface, TILE_SIZE: int, camera: Vector):
    y = 0
    for row in game_map:
        x= 0
        for tile in row:
            if tile == 1:
                pygame.draw.rect(surface, (244,24,24), pygame.Rect(x * TILE_SIZE - camera.x, y * TILE_SIZE - camera.y, TILE_SIZE,TILE_SIZE))
                # surface.blit(terrain, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 2:
                pygame.draw.rect(surface, (244,24,24), pygame.Rect(x * TILE_SIZE- camera.x, y * TILE_SIZE - camera.y, TILE_SIZE,TILE_SIZE), width = 0, border_radius = 2)
                # surface.blit(ground, (x * TILE_SIZE, y * TILE_SIZE))
            # if tile != 0:
            #     tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,TILE_SIZE))
            x += 1
        y += 1