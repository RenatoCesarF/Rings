import pygame
import json
import math
import random

from Engine import utils
from Engine.Vector import Vector
from Engine.Collisions.Collider import Collider
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Animator.Animation import Animation
from Engine.Camera import Camera
from Engine.Window import Window
from Engine.World.World import World
from Engine.World.Tile import Tile
from Engine.VFX.spark import Spark
from Engine.Entity import Entity

from Entities.Player import Player
from Entities.Mouse import Mouse

TILE_SIZE = 20

game_map = json.load(open("res/map.json"))

class MapMaker:
    running: bool = True
    camera: Camera
    center_point: Vector
    window: Window
    tiles: list
    mouse: Mouse

    def __init__(self):
        configs = json.load(open("config.json"))
        self.window = Window(configs)
        self.center_point = Vector(
            self.window.screen_real_size[0] / 2, self.window.screen_real_size[1] / 2
        )
        self.camera = Camera(Entity(self.center_point), self.window.screen_real_size)
        self.mouse = Mouse(self.window)
        self.clock = pygame.time.Clock()
        self.running = True

    def draw(self):
        self.window.display.fill((20, 20, 20))
        
        for tile in self.tiles:
            tile.draw(self.window.display, self.camera.position)

        self.draw_grid()
        self.window.blit_displays()
        self.mouse.draw(self.window.screen)
    def update(self):
        self.generate_tiles_with_game_map()
        self.mouse.update()
        self.camera.update()
        
        x_index = int((self.mouse.position.x + self.camera.position.x) / TILE_SIZE)
        y_index = int((self.mouse.position.y + self.camera.position.y) / TILE_SIZE)

        game_map[y_index][x_index] = 6
    
        pygame.display.update()
        self.clock.tick(60)
    def generate_tiles_with_game_map(self):
        self.tiles: Dict[Tile] = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == 0:
                    x += 1
                    continue
                self.tiles.append(
                    Tile(
                        position=Vector(x * TILE_SIZE, y * TILE_SIZE),
                        size=TILE_SIZE,
                        color_index=tile,
                    )
                )

                x += 1
            y += 1
        
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.center_point.x += 10
                if event.key == pygame.K_a:
                    self.center_point.x -= 10
                if event.key == pygame.K_w:
                    self.center_point.y -= 10
                if event.key == pygame.K_s:
                    self.center_point.y += 10

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_d:
            #         self.center_point.x += 10
            #     if event.key == pygame.K_a:
            #         self.center_point.x -= 1
            #     if event.key == pygame.K_w:
            #         self.center_point.y -=1
            #     if event.key == pygame.K_s:
            #         self.center_point.y -=1

    def draw_grid(self):
        for i in range (-30,30):
            for j in range(-30,30):
                t = Tile(Vector(i* TILE_SIZE, j * TILE_SIZE),
                        TILE_SIZE,
                        color_index=4, thikness=1)
                t.draw(self.window.display, self.camera.position)

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


game = MapMaker()
game.run()
