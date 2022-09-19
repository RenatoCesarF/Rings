import os
import pygame as pygame
import json
import math
from random import randint


from Engine.vector import Vector
from Engine.Glow import Glow
from Engine import utils
from Engine.shape import Shape
from Engine.Particle.shape_particle import ShapeParticle
from Engine.Particle.image_particle import ImageParticle
from Engine.Particle.particle_emitter import ParticleEmitter


configs = json.load(open("config.json"))

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 12)

global debugging
global game_time
debugging = True
game_time = 0
base_screen_size = configs["resolution"]
screen = pygame.display.set_mode((base_screen_size[0], base_screen_size[1]), 0, 32)
display = pygame.Surface((400, 280))
clock = pygame.time.Clock()


particleEmitionTime = 0
angle = 0
radius = 1
cursor_img = pygame.transform.scale(
    pygame.image.load("res/mouse.png").convert(), (33, 33)
)
cursor_img.set_colorkey((0, 0, 0))

particles = []
original_angle = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    display.fill((0, 40, 40))
    position = 120
    pygame.draw.rect(
        display,
        (255, 5, 5),
        pygame.Rect(position, position, 2, 2),
        width=0,
        border_radius=100,
    )

    particleEmitionTime -= 1
    if particleEmitionTime < 0:
        particles.append(
            ShapeParticle(
                Vector(position, position),
                Vector(2, 2),
                life_time=100,
                color=(255, 255, 255),
                opacity=215,
                width=2,
                height=2,
            )
        )
        particleEmitionTime = 50

    angle += 0.0002

    for i, particle in sorted(enumerate(particles), reverse=True):
        particle.life_time -= 0.1
        particle.position.x += math.sin(angle * 120)
        particle.position.y += math.cos(angle * 120)

        # particle.rotation += randint(1,10)
        particle.draw(display)

        if particle.life_time <= 0:
            particles.pop(i)

    screen.blit(
        pygame.transform.scale(display, base_screen_size),
        (
            (screen.get_width() - base_screen_size[0]) // 2,
            (screen.get_height() - base_screen_size[1]) // 2,
        ),
    )

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))

    pygame.display.update()

    clock.tick(60)
