from typing import List

import pygame
import json

from Engine.UI import UI

from Engine.Config import Config
from Engine import utils
from Engine.Vector import Vector
from Engine.World.Tile import Tile
from Engine.Camera import Camera
from Entities.Mouse import Mouse
from Engine.Window import Window

WORLD_FILE = "test.json"
game_map = json.load(open(WORLD_FILE))

TILE_SIZE = 10
VERTICAL_MAP_SIZE = len(game_map[0])
HORIZONTAL_MAP_SIZE = len(game_map)


class MapMaker:
    running: bool
    camera: Camera
    center_point: Vector
    window: Window
    tiles: List[Tile]
    mouse: Mouse
    selected_tile: Tile
    ui: UI
    configs: Config

    def __init__(self):
        self.selected_tile = Tile(
            Vector.zero(), TILE_SIZE, grid_index=Vector.zero())
        self.configs = Config("./res/config.json")
        self.window = Window(self.configs.resolution)
        self.ui = UI(
            self.configs.resolution_as_tuple(),
            "res/ui_theme.json",
            self.window.screen,
        )
        self.center_point = Vector(
            int(self.window.screen_real_size[0] / 2),
            int(self.window.screen_real_size[1] / 2),
        )
        self.camera = Camera(Vector(-30, -50), self.window.screen_real_size)
        self.mouse = Mouse(self.window)
        self.clock = pygame.time.Clock()
        self.running = True
        self.FONT = pygame.font.Font("res/Pixellari.ttf", 22)

    def update(self):
        self.time_delta = self.clock.tick(60) / 1000.0
        # self.ui.update(self.time_delta)
        self.generate_tiles_with_game_map()
        self.mouse.update()
        self.camera.update()

        x_index = int(
            (self.mouse.position.x + self.camera.position.x) / TILE_SIZE)
        y_index = int(
            (self.mouse.position.y + self.camera.position.y) / TILE_SIZE)
        self.tile_hover_index = [x_index, y_index]

        if self.mouse.left_is_pressed:
            self.change_tile_info(x_index, y_index, self.selected_tile.content)
        if self.mouse.right_is_pressed:
            self.change_tile_info(x_index, y_index, 0)

        pygame.display.update()
        self.clock.tick(60)

    def draw(self):
        self.window.display.fill((20, 20, 20))

        for tile in self.tiles:
            tile.draw(self.window.display, self.camera.position)

        self.draw_grid()

        Tile(
            Vector(20, 1),
            7,
            content=self.selected_tile.content,
            grid_index=Vector.zero(),
        ).draw(
            self.window.display,
            offset=Vector.zero(),
        )

        self.window.blit_displays()
        self.ui.write("Paint: ", Vector(1, 0))
        self.mouse.draw(self.window.screen)

    def change_tile_info(self, x_position, y_position, new_data):
        tile_is_not_valid = (
            x_position < 0
            or y_position < 0
            or y_position >= len(game_map)
            or x_position >= len(game_map[y_position])
        )
        if tile_is_not_valid:
            return

        game_map[y_position][x_position] = new_data

    def save_world(self, name: str):
        with open(name, "w") as f:
            json.dump(game_map, f, indent=2)
            print("Saving File")

    def write(self, text: str, position: Vector = Vector(10, 10)):
        utils.draw_text(
            self.FONT,
            text,
            self.window.screen,
            position,
        )

    def generate_tiles_with_game_map(self):
        self.tiles: List[Tile] = []
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
                        content=tile,
                        color=Tile.get_tile_color_by_index(tile),
                        grid_index=Vector(x, y),
                    )
                )

                x += 1
            y += 1

    def draw_grid(self):
        for i in range(0, VERTICAL_MAP_SIZE):
            for j in range(0, HORIZONTAL_MAP_SIZE):
                tile = Tile(
                    Vector(i * TILE_SIZE, j * TILE_SIZE),
                    TILE_SIZE,
                    content=4,
                    thikness=1,
                    grid_index=Vector(i, j),
                )
                tile.draw(self.window.display, self.camera.position)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_world(WORLD_FILE)
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.camera.position.x += 10
                if event.key == pygame.K_a:
                    self.camera.position.x -= 10
                if event.key == pygame.K_w:
                    self.camera.position.y -= 10
                if event.key == pygame.K_s:
                    self.camera.position.y += 10

                self.check_number_keys_input(event.key)
            # if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #     self.ui.check_events(event)

            # self.ui.manager.process_events(event)

    def check_number_keys_input(self, key):
        if key == pygame.K_1:
            self.selected_tile.content = 1
        elif key == pygame.K_2:
            self.selected_tile.content = 2
        elif key == pygame.K_3:
            self.selected_tile.content = 3
        elif key == pygame.K_4:
            self.selected_tile.content = 4
        elif key == pygame.K_0:
            self.selected_tile.content = 0

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


game = MapMaker()
game.run()
