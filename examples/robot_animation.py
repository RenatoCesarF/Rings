# If this file doenst work, copy it to main file and run from it
import pygame
from pygame import *
import json

from Engine import utils
from Engine.vector import Vector
from Engine.Animator.spriteSheet import Spritesheet
from Engine.Animator.animation import Animation


configs = json.load(open("config.json"))

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 22)


class Player:
    def __init__(self, position: Vector):
        self.position = position
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_down = False
        self.is_moving_up = False
        self.is_stand = False

    def load_animations(self):

        robot_spritesheet = Spritesheet(
            "res/sprites/robot.png",
            custom_colorkey=(127, 146, 255),
            space_between_sprites=1,
        )

        self.walking_right_animation = Animation(6, speed=0.3)
        self.walking_right_animation.load_from_spritesheet(
            robot_spritesheet,
            sprite_height=15,
            sprite_width=15,
            spritesheet_line_height=95,
        )

        self.walking_left_animation = Animation.create_mirrored_animation(
            self.walking_right_animation
        )

        self.idle_right_animation = Animation(24, speed=0.3)
        self.idle_right_animation.load_from_spritesheet(
            robot_spritesheet,
            sprite_height=14,
            sprite_width=17,
            spritesheet_line_height=49,
        )
        self.idle_right_animation.append_animation_from_same_spritesheet(
            2, spritesheet_line_height=64
        )

        self.idle_left_animation = Animation.create_mirrored_animation(
            self.idle_right_animation
        )
        self.current_animation = self.walking_left_animation

    def update(self, mx):

        if self.is_moving_left:
            self.position.x -= 1
        if self.is_moving_up:
            self.position.y -= 1
        if self.is_moving_right:
            self.position.x += 1
        if self.is_moving_down:
            self.position.y += 1

        if (
            not self.is_moving_right
            and not self.is_moving_up
            and not self.is_moving_down
            and not self.is_moving_left
        ):
            if mx > self.position.x:
                self.change_animation(self.idle_right_animation)

            else:
                self.change_animation(self.idle_left_animation)
        else:
            if mx > self.position.x:
                self.change_animation(self.walking_right_animation)
            else:
                self.change_animation(self.walking_left_animation)

    def change_animation(self, next_animation):
        last_animation = self.current_animation
        self.current_animation = next_animation

        if last_animation != self.current_animation:
            self.current_animation.reset_animation()

    def is_turned_left(self, mx, my):
        if mx > self.position.x:
            return True
        return False


global debugging
debugging = True
game_time = 0
base_screen_size = configs["resolution"]
screen = pygame.display.set_mode((base_screen_size[0], base_screen_size[1]), 0, 32)
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()

player = Player(Vector(110, 110))
player.load_animations()

cursor_img = pygame.transform.scale(
    pygame.image.load("res/mouse.png").convert(), (33, 33)
)
cursor_img.set_colorkey((0, 0, 0))


robot_spritesheet = Spritesheet(
    "res/sprites/robot.png", custom_colorkey=(127, 146, 255), space_between_sprites=1
)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            w = event.dict["size"][0]
            h = event.dict["size"][1]
            screen = pygame.display.set_mode(event.dict["size"], pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debugging = not debugging

            if event.key == pygame.K_d:
                player.is_moving_right = True
            if event.key == pygame.K_a:
                player.is_moving_left = True
            if event.key == pygame.K_w:
                player.is_moving_up = True
            if event.key == pygame.K_s:
                player.is_moving_down = True

        if event.type == pygame.KEYUP:
            player.is_not_walking = (
                not player.is_moving_right
                and not player.is_moving_up
                and not player.is_moving_down
                and not player.is_moving_left
            )

            if player.is_not_walking:
                player.is_stand = True

            if event.key == pygame.K_d:
                player.is_moving_right = False
            if event.key == pygame.K_w:
                player.is_moving_up = False
            if event.key == pygame.K_s:
                player.is_moving_down = False
            if event.key == pygame.K_a:
                player.is_moving_left = False

            if event.key == pygame.K_SPACE:
                pass

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    player.update(mx)
    display.fill((0, 20, 80))

    display.blit(
        player.current_animation.get_next_frame(),
        (player.position.x, player.position.y),
    )
    screen.blit(
        pygame.transform.scale(display, base_screen_size),
        (
            (screen.get_width() - base_screen_size[0]) // 2,
            (screen.get_height() - base_screen_size[1]) // 2,
        ),
    )

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))
    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10, 10))

    pygame.display.update()

    clock.tick(60)
