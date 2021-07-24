import pygame

def getMousePosition():
    pos = pygame.mouse.get_pos()
    return (pos)

def drawText(font,text,surface, position):
    interface_surface = font.render(text, False, "White")
    surface.blit(interface_surface,position)

