"""
A way to mannage darkness and light inside pygame, probably one of the best ones
"""

import os
import pygame
import json
  
configs = json.load(open('config.json'))
  
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 12)

global debugging
debugging = True
game_time = 0
base_screen_size = configs['resolution']
screen = pygame.display.set_mode((base_screen_size[0],base_screen_size[1]),0,32)
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()


cursor_img = pygame.transform.scale(pygame.image.load('res/mouse.png').convert(), (33, 33))
light = pygame.image.load('res/sprites/light.png')
cursor_img.set_colorkey((0, 0, 0))

entities = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.VIDEORESIZE:
            w = event.dict['size'][0]
            h = event.dict['size'][1]
            screen=pygame.display.set_mode(event.dict['size'],pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1 :
                debugging = not debugging
            if event.key == pygame.K_SPACE:
                pass
    

    display.fill((0,0,40))


    pygame.draw.rect(display, (255,10,10), 
                     pygame.Rect(10, 10, 50,50),border_radius = 0)

 
    darkness = pygame.surface.Surface((300,200))
    darkness.fill(pygame.color.Color('Grey'))
    darkness.blit(light,(0,0))
    display.blit(darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        

    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    pygame.display.update()
   
    clock.tick(60)
