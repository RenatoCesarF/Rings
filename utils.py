import pygame

def getMousePosition():
    pos = pygame.mouse.get_pos()
    return (pos)

def drawText(font,text,surface, position):
    interface_surface = font.render(text, False, "White")
    surface.blit(interface_surface,position)

def rotate(surface,angle,witdh, height):
    rotated_surface = pygame.transform.rotozoom(surface,angle,1)
    rotated_rect = rotated_surface.get_rect(center =(witdh, height))
    return rotated_surface,rotated_rect

