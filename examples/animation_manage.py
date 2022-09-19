# If this file doenst work, copy it to main file and run from it
import pygame
import json

from Engine import utils
from Engine.Animator.spriteSheet import Spritesheet
from Engine.Animator.animation import Animation

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


cursor_img = pygame.transform.scale(
    pygame.image.load("res/mouse.png").convert(), (33, 33)
)
cursor_img.set_colorkey((0, 0, 0))

spritesheet = Spritesheet("res/sprites/base.png")

a_stand = Animation(1)
a_stand.load_from_spritesheet(spritesheet, 24, 27, 70)
current_animation = a_stand


running_right = Animation(12, speed=0.5)
running_right.load_from_spritesheet(spritesheet, 24, 27, 38)

running_left = Animation.create_mirrored_animation(running_right)
# running_left.load_from_spritesheet(spritesheet, 24, 27, 101)


running_up = Animation(12, speed=1.5)
running_up.load_from_spritesheet(spritesheet, 24, 27, 7, isReverse=True)
next_part = Animation(12, speed=1.5)
next_part.load_from_spritesheet(spritesheet, 24, 27, 134, isReverse=True)
running_up.append_animation(next_part)

running_down = Animation(12, speed=1.5)
running_down.load_from_spritesheet(spritesheet, 24, 27, 70, isReverse=True)
next_part = Animation(12, speed=1.5)
next_part.load_from_spritesheet(spritesheet, 24, 27, 197, isReverse=True)
running_down.append_animation(next_part)

player_x = 50
player_y = 50
is_moving_left = False
is_moving_right = False
is_moving_down = False
is_moving_up = False
is_stand = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            w = event.dict["size"][0]
            h = event.dict["size"][1]
            screen = pygame.display.set_mode(event.dict["size"], pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debugging = not debugging

            if event.key == pygame.K_d:
                is_moving_right = True
            if event.key == pygame.K_a:
                is_moving_left = True
            if event.key == pygame.K_w:
                is_moving_up = True
            if event.key == pygame.K_s:
                is_moving_down = True

        if event.type == pygame.KEYUP:
            is_not_walking = (
                not is_moving_right
                and not is_moving_up
                and not is_moving_down
                and not is_moving_left
            )

            if is_not_walking:
                is_stand = True

            if event.key == pygame.K_d:
                is_moving_right = False
            if event.key == pygame.K_w:
                is_moving_up = False
            if event.key == pygame.K_s:
                is_moving_down = False
            if event.key == pygame.K_a:
                is_moving_left = False

            if event.key == pygame.K_SPACE:
                pass

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    display.fill((0, 20, 80))
    # TODO: improve if state-mants
    if is_moving_left:
        player_x -= 1
        current_animation = running_left
    if is_moving_up:
        current_animation = running_up
        player_y -= 1
    if is_moving_right:
        current_animation = running_right
        player_x += 1
    if is_moving_down:
        current_animation = running_down
        player_y += 1

    if is_moving_right and is_moving_left:
        current_animation = a_stand
    if is_moving_down and is_moving_up:
        current_animation = a_stand
    if is_moving_down and is_moving_left and is_moving_right:
        current_animation = running_down
    if is_moving_up and is_moving_left and is_moving_right:
        current_animation = running_up

    if (
        not is_moving_right
        and not is_moving_up
        and not is_moving_down
        and not is_moving_left
    ):
        current_animation = a_stand

    display.blit(current_animation.get_next_frame(), (player_x, player_y))

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
