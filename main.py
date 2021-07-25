
import os,pygame, sys,random
from Engine.Particle.particle import Particle
from Engine.Particle.particle_emitter import ParticleEmitter 
from Engine.Vector import Vector2D
import pygame.gfxdraw as gfxdraw
import utils


# os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

SCREEN_WITH = 800
SCREEN_HEIGHT = 400

FONT = pygame.font.Font("res/Pixellari.ttf", 30)
debugging = True
screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rings")
clock = pygame.time.Clock()

particlePattern = Particle(
    0,0,
    Vector2D(0,0),
    6,
    5,
)
pe = ParticleEmitter(Vector2D(300,100), 50,particlePattern,
    False,
    Vector2D(-2,-2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1 :
                debugging = not debugging
            if event.key == pygame.K_SPACE :
                pe.fillParticleList()
        if event.type == pygame.KEYUP:
            pass

    pygame.display.update()

    screen.fill((0,0,40))
    mouse_x, mouse_y = utils.getMousePosition()
    pe.updateEmitterPosition(Vector2D(mouse_x,mouse_y))
    pe.update(screen)

    # if len(pe.particles) >0:
    #     print(int(pe.particles[0].velocity.y))
    #     print(int(pe.particles[1].velocity.y)) 
    if debugging:
        utils.drawText(FONT,str(int(clock.get_fps())),screen,(10,10))
        
    clock.tick(60)
