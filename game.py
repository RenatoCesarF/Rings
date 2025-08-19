from __future__ import annotations
import json

from typing import List

import pygame
from pygame import Surface

from Engine.debugger_draw import debugger_draw
from Engine.utils import draw_collision_rect
from Engine.Entity import Entity

from Engine.UI import UI
from Engine.Vector import Vector

from Engine.Config import config
from Engine.Camera import Camera
from Engine.Window import window

from Engine.World.World import World
from Engine.image import Image

from Entities.Mouse import ClickingState, Mouse

from unit_manager import UnitManager
from Entities.unit import Unit
from Entities.enemy import Enemy

game_map = json.load(open("test.json"))


class Globals:
    """Cluster the globall variables that
    will be used in many files and classes"""

    debugging: bool = True
    TILE_SIZE = Vector(28, 14)


class Game:
    game_time: int
    running: bool
    world: World
    mouse: Mouse
    camera: Camera
    delta_time: float
    unit_manager: UnitManager
    ui: UI
    selected_tile_position: Vector
    time_delta: float

    def __init__(self) -> None:
        self.running = True
        print(config.resolution)
        self.unit_manager = UnitManager()
        self.ui = UI(
            config.resolution_as_tuple(),
            "res/ui_theme.json",
            window.screen,
        )
        self._enemies = []
        self.world = World()
        self.mouse = Mouse(window)
        self.camera = Camera(Vector.zero(), window.screen_real_size)
        self.selected: Image = Image(
            "./res/sprites/selected.png",
        )
        self.selected.set_opacity(200)
        self.clock = pygame.time.Clock()

        self._enemies.append(Enemy(Vector(5,5), 5, 5))
        self.unit_manager.unit_list.append(Unit(Vector(9, 5), self.unit_manager))

    def update(self):
        """Update function that cluster all update functions"""
        self.time_delta = self.clock.tick(60) / 1000.0
        # self._enemies = sorted(self._enemies, key=lambda x: x.position.y)
        # self.ui.update(self.time_delta)
        self.world.update()
        self.unit_manager.update(self.time_delta)

        self.selected_tile_position = World.get_tile_position_in_grid(
            self.mouse.position, self.camera.position
        )
        self.unit_manager.selected_unit = self.unit_manager.get_unit_at_position(
            self.mouse.position, self.camera.position
        )

        for enemy in self._enemies:
            for unit in self.unit_manager.unit_list:
                unit.has_in_range(enemy)

        for enemy in self._enemies:
            enemy.update()

        if self.unit_manager.selected_unit:
            self.selected_tile_position = self.unit_manager.selected_unit.tile_position
            if self.mouse.right_is_pressed:
                self.unit_manager.remove(self.unit_manager.selected_unit)

        if self.mouse.left_is_pressed and not self.unit_manager.selected_unit:
            self.add_unit_in_tile()

        self.mouse.update()

        self.camera.update()
        pygame.display.update()

    def add_unit_in_tile(self):
        """Add a new unit in the world of tiles"""
        if not self.world.is_tile_position_valid(
            int(self.selected_tile_position.x), int(self.selected_tile_position.y)
        ):
            return

        self.unit_manager.add_unit_to_list(
            Unit(
                Vector(
                    self.selected_tile_position.x,
                    self.selected_tile_position.y,
                ),
                self.unit_manager,
            )
        )

    def draw(self):
        window.display.fill((80, 90, 90))
        self.world.draw(window.display, self.camera.position)

        self.draw_selection_square(window.display)

        self.unit_manager.draw(window.display, self.camera.position)

        for enemy in self._enemies:
            enemy.draw(window.display, self.camera.position)

        debugger_draw.draw(self.camera.position)

        window.blit_displays()
        # self.ui.draw(window.screen)
        self.ui.write(str(int(self.clock.get_fps())), Vector(0, 300))
        # self.ui.write(str(len(self.unit_manager.bullets)), Vector(0, 330))
        self.ui.write(str(self.mouse.position), Vector(0, 350))
        self.ui.write(str(self.camera.position), Vector(0, 400))
        self.ui.write(
            "have target: " + str(self.unit_manager.unit_list[0].has_entity_in_range),
            Vector(0, 380),
        )
        self.mouse.draw(window.screen)

        self.draw_top_down_view()

    def draw_top_down_view(self):
        screen_destination = window.screen
        tile_size = 20
        tile_color = (0, 178, 0)
    
        for i_row, row in enumerate(self.world.map_matrix):
            for i_tile, tile in enumerate(row):
                tile_color = (0, 178, 0)
                pygame.draw.rect(
                    screen_destination,
                    (200, 0, 0),
                    pygame.Rect(
                        tile.grid_index.x * tile_size,
                        tile.grid_index.y * tile_size,
                        tile_size,
                        tile_size,
                    ),
                    width=1,
                )
                if tile.content == 0:
                    continue
    
                if self.selected_tile_position.is_equal(Vector(i_tile, i_row)):
                    tile_color = (0, 78, 0)
    
                pygame.draw.rect(
                    screen_destination,
                    tile_color,
                    pygame.Rect(
                        tile.grid_index.x * tile_size,
                        tile.grid_index.y * tile_size,
                        18,
                        18,
                    ),
                    width=0,
                )
    
        for unit in self.unit_manager.unit_list:
            unit_color = (0, 0, 200)
    
            if unit == self.unit_manager.selected_unit:
                unit_color = (200, 200, 0)
                range_color = (200, 200, 40)
    
                if unit.has_entity_in_range:
                    range_color = (200, 0, tile_size)
    
                # DRAW RANGE
                pygame.draw.circle(
                    screen_destination,
                    range_color,
                    (
                        (unit.tile_position.x * tile_size) + 8,
                        (unit.tile_position.y * tile_size) + 8,
                    ),
                    unit.fire_range,
                    3,
                )
    
            # DRAW UNIT
            pygame.draw.circle(
                screen_destination,
                unit_color,
                ((unit.tile_position.x * tile_size) + 8 , (unit.tile_position.y * tile_size) + 8),
                5,
                0,
            )
    
        for enemy in self._enemies:
            pygame.draw.circle(
                screen_destination,
                (255, 0, 0),
                ((enemy.position.x * tile_size ) + 8, (enemy.position.y * tile_size )+ 8),
                5,
                0,
            )
    
        # position = World.get_tile_position_in_grid(self., Vector(0, 0))

    def draw_selection_square(self, surface: Surface):
        is_selectable = self.world.is_tile_position_valid(
            int(self.selected_tile_position.x), int(self.selected_tile_position.y)
        )
        if not is_selectable:
            return

        self.selected.draw(
            surface,
            window.to_isometric_position_from_vector(self.selected_tile_position),
            self.camera.position,
        )

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Globals.debugging = not Globals.debugging

                # if event.key == pygame.K_f:
                #     self._enemies.append(Enemy(self.mouse.position + self.camera.position, 5, 5))

                if event.key == pygame.K_j:
                    self._enemies.pop()
                
                if event.key == pygame.K_a:
                    # self.camera.position.x -= 10
                    self._enemies[0].position.x -= 0.5

                if event.key == pygame.K_d:
                    # self.camera.position.x += 5
                    self._enemies[0].position.x += 0.5

                if event.key == pygame.K_s:
                    self._enemies[0].position.y += 0.5
                    # self.camera.position.y += 5

                if event.key == pygame.K_w:
                    self._enemies[0].position.y -= 0.5
                    # self.camera.position.y -= 5

                if event.key == pygame.K_1:
                    self.mouse.set_state(ClickingState.Create)

                if event.key == pygame.K_d:
                    self.mouse.set_state(ClickingState.Delete)

                if event.key == pygame.K_s:
                    self.mouse.set_state(ClickingState.Select)

                if event.key == pygame.K_SPACE:
                    for unit in self.unit_manager.unit_list:
                        unit.set_target(self._enemies[0])
                        unit.fire()
            # if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #     self.ui.check_events(event)

            # self.ui.manager.process_events(event)

    def run(self) -> None:
        while self.running:
            self.process_events()
            self.update()
            self.draw()


