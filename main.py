#If this file doenst work, copy it to main file and run from it
import pygame
from pygame import *
import json

from Engine import utils
from Engine.Vector import Vector
from Engine.Collisions.Collider import Collider
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Animator.Animation import Animation
from Entities.Player import Player

configs = json.load(open('config.json'))
  
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 22)
#    // "resolution": [1280, 720],

global debugging

game_time = 0
base_screen_size = configs['resolution']
screen = pygame.display.set_mode((base_screen_size[0],base_screen_size[1]),0,32)

display = pygame.Surface((300, 200))
clock = pygame.time.Clock()

camera = Vector(0,0)
player = Player(Vector(10,10))
player.load_animations()

TILE_SIZE = 20

game_map = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
[0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1],
[0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

cursor_img = pygame.transform.scale(pygame.image.load('res/mouse.png').convert(), (44, 44))
cursor_img.set_colorkey((255, 0, 0))


debugging = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            exit()
        if event.type==pygame.VIDEORESIZE:
            w = event.dict['size'][0]
            h = event.dict['size'][1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1 :
                debugging = not debugging

            if event.key == pygame.K_SPACE:
                player.speed = 5
            if event.key == pygame.K_d:
                player.is_moving_right = True
            if event.key == pygame.K_a:
                player.is_moving_left = True
            if event.key == pygame.K_w:
                player.is_moving_up = True
            if event.key == pygame.K_s:
                player.is_moving_down = True

        if event.type == pygame.KEYUP:
            player.is_not_walking = not player.is_moving_right  and not player.is_moving_up  and not player.is_moving_down and not player.is_moving_left

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
                player.speed = 1
       
            if event.key == pygame.K_SPACE:
                pass
    

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    camera.x += (player.position.x - camera.x - 140) / 10
    camera.y += (player.position.y - camera.y - 100) / 10
    scroll = camera
    scroll.x = int(scroll.x)
    scroll.y = int(scroll.y)

    display.fill((30,30,30))
        
    collision_tiles = []
    tile_rects =[] 


    y = 0
    for row in game_map:
        x= 0
        for tile in row:
            if tile == 1:
                pygame.draw.rect(display, (204,24,24), pygame.Rect(x * TILE_SIZE - camera.x, y * TILE_SIZE - camera.y, TILE_SIZE,TILE_SIZE))
            if tile == 2:
                pygame.draw.rect(display, (204,24,24), pygame.Rect(x * TILE_SIZE- camera.x, y * TILE_SIZE - camera.y, TILE_SIZE,TILE_SIZE), width = 0, border_radius = 2)
            if tile != 0:
                collision_tiles.append(Collider(Vector(x * TILE_SIZE, y * TILE_SIZE), TILE_SIZE,TILE_SIZE))
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,TILE_SIZE))
            x += 1
        y += 1

    player.update(mx - 18, collision_tiles)
    player.draw(display,camera,debugging)
    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))

    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10,10))


    pygame.display.update()
   
    clock.tick(60)