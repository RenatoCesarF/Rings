import os
import pygame
import json
import math
import random

from Engine.Vector import Vector2D
from Engine import utils
from Engine.shape import Shape
from Engine.Particle.shape_particle import ShapeParticle
from Engine.Particle.image_particle import ImageParticle
from Engine.Particle.particle_emitter import ParticleEmitter 
from Engine.Animation.SpriteSheet import Spritesheet
from Engine.Animation.animation import Animation
  
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

cursor_img.set_colorkey((0, 0, 0))


spritesheet = Spritesheet("res/sprites/base.png")
animation = Animation(12,speed=0.5)
animation.load_from_spritesheet(spritesheet, 24, 27, 38)

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
    

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    display.fill((0,20,80))
        
    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), display, (10,10))
  
  
    display.blit(animation.get_next_frame(),(50,80))

    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))


    pygame.display.update()
   
    clock.tick(60)
