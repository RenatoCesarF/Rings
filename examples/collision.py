import pygame
from pygame import *
import json

from Engine import utils
from Engine.vector import Vector
from Engine.Animator.spriteSheet import Spritesheet
from Engine.Animator.animation import Animation
from Entities.Player import Player
from Engine.Collisions.collider import Collider


class Squares:
    def __init__(
        self, position: Vector, width: int, height: int, color: tuple = (200, 0, 0)
    ):
        self.color = color
        self.position = position
        self.width = width
        self.height = height
        self.collision = Collider(position, width, height)


configs = json.load(open("config.json"))

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 22)
#    // "resolution": [1280, 720],

global debugging

debugging = True
game_time = 0
base_screen_size = configs["resolution"]
screen = pygame.display.set_mode((base_screen_size[0], base_screen_size[1]), 0, 32)

display = pygame.Surface((300, 200))
clock = pygame.time.Clock()


square_a = Squares(Vector(50, 50), 30, 30)
square_a.collision.speed = Vector(2, 2)
square_b = Squares(Vector(150, 75), 50, 20, color=(0, 200, 0))
square_b.collision.speed = Vector(0, 2)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            w = event.dict["size"][0]
            h = event.dict["size"][1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debugging = not debugging

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    display.fill((30, 30, 30))

    square_a.position.x = mx
    square_a.position.y = my

    square_a.collision.collision_rect.x = square_a.position.x
    square_a.collision.collision_rect.y = square_a.position.y

    square_a.color = (200, 0, 0)

    square_a.collision.check_colliding_with(square_b.collision)

    if square_a.collision.is_colliding:
        square_a.color = (0, 0, 200)

    pygame.draw.rect(
        display,
        square_a.color,
        pygame.Rect(
            square_a.position.x, square_a.position.y, square_a.width, square_a.height
        ),
        width=0,
    )
    pygame.draw.rect(
        display,
        square_b.color,
        pygame.Rect(
            square_b.position.x, square_b.position.y, square_b.width, square_b.height
        ),
        width=0,
    )

    screen.blit(
        pygame.transform.scale(display, base_screen_size),
        (
            (screen.get_width() - base_screen_size[0]) // 2,
            (screen.get_height() - base_screen_size[1]) // 2,
        ),
    )

    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10, 10))

    pygame.display.update()

    clock.tick(60)
