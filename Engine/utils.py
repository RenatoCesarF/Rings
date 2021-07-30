"""Functions that don't have a specific folder or class yet"""

import pygame

def get_mouse_position():
    x,y = pygame.mouse.get_pos()
    pos = (x // 3 * 3 + 1, y // 3 * 3 + 1)
    return (pos)

def draw_text(font,text,surface, position):
    interface_surface = font.render(text, False, "White")
    surface.blit(interface_surface,position)

def rotate(surface,angle,witdh, height):
    rotated_surface = pygame.transform.rotozoom(surface,angle,1)
    rotated_rect = rotated_surface.get_rect(center =(witdh, height))
    return rotated_surface,rotated_rect

