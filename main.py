#If this file doenst work, copy it to main file and run from it
import pygame
from pygame import *
import json

from Engine import utils
from Engine.Vector import Vector
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

debugging = True
game_time = 0
base_screen_size = configs['resolution']
screen = pygame.display.set_mode((base_screen_size[0],base_screen_size[1]),0,32)

display = pygame.Surface((300, 200))
clock = pygame.time.Clock()

camera = Vector(0,0)
player = Player(Vector(110,110))
player.load_animations()

TILE_SIZE = 16

game_map = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

cursor_img = pygame.transform.scale(pygame.image.load('res/mouse.png').convert(), (33, 33))
cursor_img.set_colorkey((0, 0, 0))


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

    tile_rects =[] 
    utils.fill_game_map(game_map,display,TILE_SIZE,scroll);

    player.update(mx- 24)



    display.blit(player.get_frame(),(player.position.x-camera.x,player.position.y-camera.y))
    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))

    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10,10))


    pygame.display.update()
   
    clock.tick(60)