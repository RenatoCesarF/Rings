import os
import pygame
import math
import random

from Engine.Vector import Vector2D
from Engine import utils
from Engine.shape import Shape
from Engine.Particle.shape_particle import ShapeParticle
from Engine.Particle.image_particle import ImageParticle
from Engine.Particle.particle_emitter import ParticleEmitter 


game_time = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
particles = []
pygame.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")

FONT = pygame.font.Font("res/Pixellari.ttf", 12)

debugging = True
game_time = 0
base_screen_size = [920, 680]
screen = pygame.display.set_mode((base_screen_size[0],base_screen_size[1]),0,32)
display = pygame.Surface((300, 200))
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
cursor_img = pygame.transform.scale(pygame.image.load('res/mouse.png').convert(), (33, 33))
cursor_img.set_colorkey((0, 0, 0))

leaft = pygame.image.load('res/leaft.png').convert()
leaft.set_colorkey((0, 0, 0))

#BUG: velocity is not beeing passed as float
particle_pattern = ImageParticle(leaft,Vector2D(140,140),Vector2D(0.05,0.05), width=110, height=110,
                                    life_time = 4)

pe = ParticleEmitter(Vector2D(10,200), 120, particle_pattern, False,
                        Vector2D(-2,-2))

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
                pe.add_particle()
            if event.key == pygame.K_0:
                pe.amount +=10
                
            if event.key == pygame.K_1:
                pe.start()

        if event.type == pygame.KEYUP:
            pass

    #-----Update------
    game_time +=1
    display.fill((0,0,40))
    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    pe.update(display)
    pe.update_emitter_position(Vector2D(mx,  my))

    if len(pe.particles) > 0:
        utils.draw_text(FONT, str(len(pe.particles)), display, (10,50))
    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), display, (10,10))

    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))
    pygame.display.update()
   
    clock.tick(120)


if __name__ == '__main__':

    main()