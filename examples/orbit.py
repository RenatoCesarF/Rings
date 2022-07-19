from typing import Tuple
import pygame as pygame
import json
import math


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")

FONT = pygame.font.Font("res/Pixellari.ttf", 12)

screen = pygame.display.set_mode((920, 680), 0, 32)
display = pygame.Surface((920, 680))
clock = pygame.time.Clock()


particleEmitionTime = 0


class Orbit:
    def __init__(
        self,
        position: Tuple,
        size: int,
        speed: float,
        angle: int,
    ) -> None:
        self.position = position
        self.gravitation_center = position
        self.size = size
        self.speed = speed
        self.angle = angle
        self.gravitation_size = 141


planet = Orbit([450, 276], size=10, speed=21, angle=38)
angle2 = 4
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                angle2 += 20

            if event.key == pygame.K_LEFT:
                angle2 -= 20
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # display.fill((0,40,40))

    planet.position = [planet.gravitation_center[0], planet.gravitation_center[1]]

    planet.position[0] += math.floor(
        math.sin(planet.angle * 0.0018) * (planet.gravitation_size + planet.size)
    )
    planet.position[1] += math.floor(
        math.cos(planet.angle * 0.0018) * (planet.gravitation_size + planet.size)
    )

    planet.position[0] -= math.sin(angle2 * 0.018) * 10
    planet.position[1] -= math.cos(angle2 * 0.018) * 10

    planet.angle += planet.speed
    angle2 += 300

    pygame.draw.circle(display, (255, 5, 0), planet.gravitation_center, 2, 0)
    pygame.draw.circle(display, (2, 255, 5), planet.position, planet.size, 0)

    screen.blit(
        pygame.transform.scale(display, [920, 680]),
        ((screen.get_width() - 920) // 2, (screen.get_height() - 680) // 2),
    )

    pygame.display.update()

    clock.tick(60)
