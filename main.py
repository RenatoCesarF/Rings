import os
import pygame

from Engine.Vector import Vector2D
from Engine import utils
from Engine.Particle.shape_particle import ShapeParticle
from Engine.shape import Shape
from Engine.Particle.particle_emitter import ParticleEmitter 

def main():
    debugging = True
    screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT), pygame.RESIZABLE)
    
    clock = pygame.time.Clock()

    particle_pattern = ShapeParticle(Vector2D(0,0),Vector2D(1,1), width=11, height=11,
                                life_time = 2, shape = Shape.Rect)

    pe = ParticleEmitter(Vector2D(10,200), 120, particle_pattern, False,
                         Vector2D(-2,-2))
   
    particle_pattern.describe()
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


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()
    pygame.init()
    pygame.display.set_caption("Rings")

    FONT = pygame.font.Font("res/Pixellari.ttf", 24)
    SCREEN_WITH = 800
    SCREEN_HEIGHT = 400

    main()