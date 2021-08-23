from typing import Tuple
import pygame as pygame
import json
import math

  
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")

FONT = pygame.font.Font("res/Pixellari.ttf", 12)

screen = pygame.display.set_mode((920, 680),0,32)
display = pygame.Surface((920, 680))
clock = pygame.time.Clock()


particleEmitionTime = 0

class Orbit:
    def __init__(self,position: Tuple,radius: int,speed: float,angle: int,) -> None:
        self.position = position
        self.center_position = position
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.gravitation_radius = 140

planet = Orbit([450,276], radius = 20, speed = 0.5, angle = 180)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    display.fill((0,40,40))

    planet.position = [planet.center_position[0],planet.center_position[1]]

    planet.position[0] += math.floor(math.sin(planet.angle * 0.017) * (planet.gravitation_radius + planet.radius))
    planet.position[1] += math.floor(math.cos(planet.angle * 0.017) * (planet.gravitation_radius + planet.radius))

    pygame.draw.circle(display, (255,5,0),planet.center_position,planet.gravitation_radius,0)
    pygame.draw.circle(display, (2,255,5),planet.position,planet.radius,0)

    planet.angle += planet.speed


    screen.blit(pygame.transform.scale(display, [920, 680]),
                ((screen.get_width() - 920) // 2,
                (screen.get_height() - 680) // 2))

    pygame.display.update()
   
    clock.tick(60)
