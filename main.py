#If this file doenst work, copy it to main file and run from it
import pygame
import json

from Engine import utils
from Engine.Animation.SpriteSheet import Spritesheet
from Engine.Animation.Animation import Animation
  
configs = json.load(open('config.json'))
  
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)
pygame.display.set_caption("Rings")
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("res/Pixellari.ttf", 22)

global debugging
debugging = True
game_time = 0
base_screen_size = configs['resolution']
screen = pygame.display.set_mode((base_screen_size[0],base_screen_size[1]),0,32)
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()


cursor_img = pygame.transform.scale(pygame.image.load('res/mouse.png').convert(), (33, 33))
cursor_img.set_colorkey((0, 0, 0))


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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pass
    

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 3
    my -= (screen.get_height() - base_screen_size[1]) // 3
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    display.fill((0,20,80))

    screen.blit(pygame.transform.scale(display, base_screen_size),
                ((screen.get_width() - base_screen_size[0]) // 2,
                (screen.get_height() - base_screen_size[1]) // 2))

    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))
    if debugging:
        utils.draw_text(FONT, "FPS: " + str(int(clock.get_fps())), screen, (10,10))


    pygame.display.update()
   
    clock.tick(60)
