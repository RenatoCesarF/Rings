import os
import pygame

from Engine.Vector import Vector2D
from Engine import utils
from Engine.Particle.particle import Particle,Shape
from Engine.Particle.particle_emitter import ParticleEmitter 

os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

SCREEN_WITH = 800
SCREEN_HEIGHT = 400

FONT = pygame.font.Font("res/Pixellari.ttf", 24)
debugging = True
screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rings")
clock = pygame.time.Clock()

# particle_pattern = Particle(x=0, y=0,velocity=Vector2D(0,0), width=11, height=11,
#                             life_time=2, shape=Shape.Rect)

particle_pattern = Particle.fromImage("S")
pe = ParticleEmitter(Vector2D(10,200), 10, particle_pattern, True,
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
    pygame.display.update()

    screen.fill((0,0,40))

    pe.update(screen)

    if len(pe.particles) > 0:
        utils.draw_text(FONT, str(len(pe.particles)), screen, (10,50))
    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10,10))

    clock.tick(60)
