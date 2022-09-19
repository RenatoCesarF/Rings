# If this file doenst work, copy it to main file and run from it
import pygame
import json
import math
import random

from Engine.VFX.spark import Spark
from Engine import utils
from Engine.vector import Vector
from Engine.Animator.spriteSheet import Spritesheet
from Engine.Animator.animation import Animation
from Engine.Particle.shape_particle import ShapeParticle
from Engine.shape import Shape


configs = json.load(open("config.json"))

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 22)


global debugging
debugging = True
game_time = 0
base_screen_size = configs["resolution"]
screen = pygame.display.set_mode((base_screen_size[0], base_screen_size[1]), 0, 32)
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()


sparks = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            exit()

    display.fill((0, 20, 20))

    s = Spark(
        Vector(50, 50),
        math.radians(random.randint(0, 360)),
        speed=random.randint(1, 3),
        color=(255, 255, 255),
    )
    sparks.append(s)

    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.color = (
            random.randint(40, 240),
            random.randint(40, 240),
            random.randint(40, 240),
        )
        spark.draw(display)
        if not spark.alive:
            sparks.pop(i)

    screen.blit(
        pygame.transform.scale(display, base_screen_size),
        (
            (screen.get_width() - base_screen_size[0]) // 2,
            (screen.get_height() - base_screen_size[1]) // 2,
        ),
    )

    pygame.display.update()

    clock.tick(60)
