from __future__ import annotations

from typing import Dict, List,Any, Tuple


import pygame
import pygame_gui

from Engine import utils
from Engine.entity import Entity
from Engine.UI import UI
from Engine.vector import Vector

from Engine.config import Config
from Engine.config import TILE_SIZE
from Engine.camera import Camera
from Engine.window import Window
from Engine.World.Tile import Tile
from Engine.World.world import World
from Engine.image import Image

from Entities.Mouse import ClickingState, Mouse

from unit_manager import UnitManager
from unit import Unit

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
    delta_time: float
    unit_manager: UnitManager
    ui: UI

    def __init__(self) -> None:
        # self.unit_manager = UnitManager(self)
        self.running = True
        self.configs = Config("./res/config.json")
        self.window = Window(self.configs.resolution)
        self.ui = UI(
            self.configs.resolution_as_tuple(),
            'res/ui_theme.json',
            self.window.screen
        )
        self.world = World()
        self.mouse = Mouse(self.window)
        self.camera = Camera(None, self.window.screen_real_size)
        self.selected: Image = Image('./res/sprites/selected.png',)
        self.selected.set_opacity(200)
        self.clock = pygame.time.Clock()

    def update(self):
        self.time_delta = self.clock.tick(60)/1000.0
        self.ui.update(self.time_delta)
        self.world.update()
        
        self.selected_tile_position = World.get_tile_position_in_grid(
            self.mouse.position,
            self.camera.position
        )
        
        self.mouse.update()
        self.camera.update()
        pygame.display.update()
    
    def draw(self):
        self.window.display.fill((80, 90, 90))
        self.world.draw(self.window.display, self.camera.position)
        # self.world.draw_grid(self.window.display, self.camera.position)
 
        self.selected.draw(
            self.window.display,
            Window.to_screen(
                self.selected_tile_position.x,
                self.selected_tile_position.y
            ),
            self.camera.position)
        self.window.blit_displays()
        self.ui.draw(self.window.screen)
        self.ui.write(str(self.selected_tile_position), Vector(0,30))
        self.ui.write(str(World.get_uppon_tile_number(self.mouse.position, self.camera.position)), Vector(0,50))
        self.ui.write(str(int(self.clock.get_fps())), Vector(0,10))
        self.mouse.draw(self.window.screen)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Globals.debugging = not Globals.debugging

                if event.key == pygame.K_a:
                    self.camera.position.x-=10
    
                if event.key == pygame.K_d:
                    self.camera.position.x+=10
              
                if event.key == pygame.K_s:
                    self.camera.position.y+=10
                
                if event.key == pygame.K_w:
                    self.camera.position.y-=10
                    
                    
                if event.key == pygame.K_1:
                    self.mouse.set_state(ClickingState.Create)
                    
                if event.key == pygame.K_d:
                    self.mouse.set_state(ClickingState.Delete)
                    
                if event.key == pygame.K_s:
                    self.mouse.set_state(ClickingState.Select)

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
