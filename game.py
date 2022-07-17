import pygame
import json
from math import sin, cos, floor

from Engine import utils
from Engine.Vector import Vector
from Engine.Collisions.Collider import Collider
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Animator.Animation import Animation
from Engine.Camera import Camera
from Engine.Window import Window
from Engine.World.World import World

from Entities.Player import Player
from Entities.Mouse import Mouse


class Globals:
    debugging = True

class Game:
    __entities: list
    game_time: int
    player: Player
    window: Window
    world: World
    mouse: Mouse
    camera: Camera

    def __init__(self):
        configs = json.load(open("config.json"))
        self.window = Window(configs)
        self.mouse = Mouse(self.window)
        self.world = World()
        self.player = Player(self)
        self.player.load_animations()
        self.camera = Camera(self.player, self.window.screen_real_size)

        self.running = True
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.Font("res/Pixellari.ttf", 22)

    def update(self):
        pygame.display.update()

        self.world.update()
        self.mouse.update()
        self.player.update()
        self.camera.update()
        
        # scroll = self.camera
        # scroll.x = int(scroll.x)
        # scroll.y = int(scroll.y)

        self.clock.tick(60)

    def draw(self):
        self.window.display.fill((30, 30, 30))
        self.world.draw(self.window.display, self.camera.position)
        self.player.draw(self.window.display, self.camera.position)

        self.window.blit_displays()

        self.draw_fps()
        self.mouse.draw(self.window.screen)

    def draw_fps(self):
        if not Globals.debugging:
            return
        utils.draw_text(
            self.FONT,
            "FPS: " + str(int(self.clock.get_fps())),
            self.window.screen,
            (10, 10),
        )

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Globals.debugging = not Globals.debugging
                    self.camera.set_target(self.mouse)

                if event.key == pygame.K_SPACE:
                    self.player.speed = 5
                if event.key == pygame.K_d:
                    self.player.is_moving_right = True
                if event.key == pygame.K_a:
                    self.player.is_moving_left = True
                if event.key == pygame.K_w:
                    self.player.is_moving_up = True
                if event.key == pygame.K_s:
                    self.player.is_moving_down = True

            if event.type == pygame.KEYUP:
                self.player.is_not_walking = (
                    not self.player.is_moving_right
                    and not self.player.is_moving_up
                    and not self.player.is_moving_down
                    and not self.player.is_moving_left
                )

                if self.player.is_not_walking:
                    self.player.is_stand = True
                if event.key == pygame.K_d:
                    self.player.is_moving_right = False
                if event.key == pygame.K_w:
                    self.player.is_moving_up = False
                if event.key == pygame.K_s:
                    self.player.is_moving_down = False
                if event.key == pygame.K_a:
                    self.player.is_moving_left = False

                if event.key == pygame.K_SPACE:
                    self.player.speed = 1

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


game = Game().run()