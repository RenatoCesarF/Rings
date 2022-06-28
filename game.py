import pygame
import json
from math import sin, cos, floor

from Engine import utils
from Engine.Vector import Vector
from Engine.Collisions.Collider import Collider
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Animator.Animation import Animation

from Entities.Player import Player
from Entities.Mouse import Mouse
from Engine.World import World


class Globals:
    debugging = True


class Game:
    world: any
    entities: list
    game_time: int
    player: Player
    world: World
    mouse: Mouse
    camera: Vector()

    def __init__(self):
        self.init_pygame()
        self.mouse = Mouse(self)
        self.world = World()
        self.camera = Vector()
        self.player = Player(Vector(), self)
        self.player.load_animations()
        # self.entities = init_entities()0

    def init_pygame(self):
        configs = json.load(open("config.json"))
        self.running = True

        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(32)
        pygame.display.set_caption("Rings")
        pygame.mouse.set_visible(False)
        self.FONT = pygame.font.Font("res/Pixellari.ttf", 22)
        self.base_screen_size = configs["resolution"]

        self.screen = pygame.display.set_mode(
            (self.base_screen_size[0], self.base_screen_size[1]), 0, 32
        )

        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        self.screen_real_size = (300, 200)

    def update(self):
        pygame.display.update()

        self.world.update()
        self.mouse.update()
        self.player.update()
        self.camera.x = self.player.position.x + 7 - self.screen_real_size[0] / 2
        self.camera.y = self.player.position.y + 7 - self.screen_real_size[1] / 2

        # scroll = self.camera
        # scroll.x = int(scroll.x)
        # scroll.y = int(scroll.y)

        self.clock.tick(60)

    def draw(self):
        self.display.fill((30, 30, 30))
        self.world.draw(self.display, self.camera)
        self.player.draw(self.display, self.camera)

        self.screen.blit(
            pygame.transform.scale(self.display, self.base_screen_size),
            (
                (self.screen.get_width() - self.base_screen_size[0]) // 2,
                (self.screen.get_height() - self.base_screen_size[1]) // 2,
            ),
        )

        self.draw_fps()
        self.mouse.draw(self.screen)

    def draw_fps(self):
        if not Globals.debugging:
            return
        utils.draw_text(
            self.FONT,
            "FPS: " + str(int(self.clock.get_fps())),
            self.screen,
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
