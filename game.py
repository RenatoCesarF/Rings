from __future__ import annotations

from typing import Dict, List,Any, Tuple

import math 
import pygame
from pygame.rect import Rect
from pygame.surface import Surface

import pygame
import pygame_gui
from requests_mock import mock

from Engine.utils import draw_collision_rect
from Engine.entity import Entity
from Engine.UI import UI
from Engine.vector import Vector

from Engine.config import Config
from Engine.config import TILE_SIZE
from Engine.camera import Camera
from Engine.window import Window
from Engine.World.tile import Tile
from Engine.World.world import World
from Engine.image import Image

from Entities.mouse import ClickingState, Mouse

from unit_manager import UnitManager
from Entities.unit import Unit
from Entities.bullet import Bullet
from Entities.enemy import Enemy

class Globals:
    debugging: bool = True

class Game:
    _entities: List[Entity]
    configs: Config
    game_time: int
    running: bool
    window: Window
    world: World
    mouse: Mouse
    camera: Camera
    _entities: List[Entity]
    delta_time: float
    unit_manager: UnitManager
    ui: UI
    ent: pygame.Rect
    def __init__(self) -> None:
        self.unit_manager = UnitManager(self)
        self.running = True
        self.ent = pygame.Rect(0, 0, 50, 50)
        self.configs = Config("./res/config.json")
        self.window = Window(self.configs.resolution)
        self.ui = UI(
            self.configs.resolution_as_tuple(),
            'res/ui_theme.json',
            self.window.screen
        )
        self._entities = []
        self.world = World()
        self.mouse = Mouse(self.window)
        self.camera = Camera(None, self.window.screen_real_size)
        self.selected: Image = Image('./res/sprites/selected.png',)
        self.selected.set_opacity(200)
        self.clock = pygame.time.Clock()
        self._entities.append(
            Enemy(Vector(10,60), 20, 20)
        )
        self.unit_manager.unit_list.append(Unit(Vector(9,5), self.unit_manager))

    def update(self):
        self.time_delta = self.clock.tick(60)/1000.0
        self._entities = sorted(self._entities,key= lambda x:x.position.y)
        self.ui.update(self.time_delta)
        self.world.update()
        self.unit_manager.update(self.time_delta)

        self.selected_tile_position = World.get_tile_position_in_grid(
            self.mouse.position,
            self.camera.position
        )
        self.unit_manager.selected_unit = self.unit_manager.get_unit_at_position(
           self.mouse.position,
           self.camera.position
        )
        e = Entity(Vector())
        e.collision_rect = self.ent
        if len(self.unit_manager.unit_list):
            self.unit_manager.unit_list[0].is_in_range(e)

        for ent in self._entities:
            ent.update()
        
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
        if not self.world.is_tile_position_valid(
                self.selected_tile_position.x,
                self.selected_tile_position.y
            ):
            return
        
        self.unit_manager.add_unit_to_list(
            Unit(
                Vector(self.selected_tile_position.x,self.selected_tile_position.y),
                self.unit_manager
            )
        )

    def draw(self):
        self.window.display.fill((80, 90, 90))
        self.world.draw(self.window.display, self.camera.position)

        self.draw_selection_square(self.window.display)

        self.unit_manager.draw(self.window.display, self.camera.position)

        for ent in self._entities:
            ent.draw(self.window.display, self.camera.position)

        # ======================
        draw_collision_rect(self.ent, self.window.display, self.camera.position)

        self.window.blit_displays()
        self.ui.draw(self.window.screen)
        self.ui.write(str(int(self.clock.get_fps())), Vector(0,10))
        self.ui.write(str(len(self.unit_manager.bullets)), Vector(0, 30))
        # self.ui.write("Selected Tile: "  + str(self.selected_tile_position.as_tuple), Vector(0,30))
        self.mouse.draw(self.window.screen)

    def draw_selection_square(self, surface: Surface):
        is_selectable = self.world.is_tile_position_valid(
            self.selected_tile_position.x, 
            self.selected_tile_position.y
        )
        if not is_selectable:
            return
        
        self.selected.draw(
            surface,
            Window.to_isometric_position_from_vector(
                self.selected_tile_position
            ),
            self.camera.position
        )
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Globals.debugging = not Globals.debugging

                if event.key == pygame.K_a:
                    # self.camera.position.x-=10
                    self.ent.x-=5
    
                if event.key == pygame.K_d:
                    # self.camera.position.x+=5
                    self.ent.x+=5
              
                if event.key == pygame.K_s:
                    self.ent.y+=5
                    # self.camera.position.y+=5
                
                if event.key == pygame.K_w:
                    self.ent.y-=5
                    # self.camera.position.y-=5
                    
                    
                if event.key == pygame.K_1:
                    self.mouse.set_state(ClickingState.Create)
                    
                if event.key == pygame.K_d:
                    self.mouse.set_state(ClickingState.Delete)
                    
                if event.key == pygame.K_s:
                    self.mouse.set_state(ClickingState.Select)

                if event.key == pygame.K_SPACE:
                    for unit in self.unit_manager.unit_list:
                        unit.set_target(self._entities[0])
                        unit.fire()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.ui.check_events(event)

            self.ui.manager.process_events(event)

    def run(self) -> None:
        while self.running:
            self.process_events()
            self.update()
            self.draw()

game = Game()
game.run()
