import os,pygame, sys
import pygame.gfxdraw as gfxdraw
import utils

os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

SCREEN_WITH = 800
SCREEN_HEIGHT = 400

FONT = pygame.font.Font("res/Pixellari.ttf", 30)

screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rings")
clock = pygame.time.Clock()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    utils.drawText(FONT,"A",screen,(100,100))
    pygame.display.update()


    clock.tick(60)


