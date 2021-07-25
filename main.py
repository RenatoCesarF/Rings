import os,pygame, sys,random
from Engine.Particle.particle import Particle
import pygame.gfxdraw as gfxdraw
import utils


# os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

SCREEN_WITH = 800
SCREEN_HEIGHT = 400

FONT = pygame.font.Font("res/Pixellari.ttf", 30)

screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rings")
clock = pygame.time.Clock()

particles = []
def emmit():
    mouse_x, mouse_y = utils.getMousePosition()
    for i in range (0,20):
        particles.append(Particle(mouse_x,mouse_y,random.randint(6,12),random.randint(0,20)/10 - 1,-random.randint(0,20),5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            print("down")
        if event.type == pygame.KEYUP:
            emmit()


    pygame.display.update()

    screen.fill((0,0,40))

    i = 0
    while i < len(particles):
        particles[i].Update()
        particles[i].Draw(screen)
        if particles[i].lifeTime <= 0:
            particles.pop(i)
        else:
            i += 1
    # for particle in particles:
    #     particle.Draw(screen)
    #     if particle.lifeTime<=0:
    #         particles.remove(particle)

    utils.drawText(FONT,str(int(clock.get_fps())),screen,(10,10))
    utils.drawText(FONT,str(len(particles)),screen,(10,40))
    if len(particles) >=1:
        utils.drawText(FONT,str(particles[0].lifeTime),screen,(10,70))
    clock.tick(60)


