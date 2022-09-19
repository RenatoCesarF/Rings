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
from Engine.World.World import World
from Engine.image import Image

from Entities.Mouse import ClickingState, Mouse

from unit_manager import UnitManager
from unit import Unit

class Globals:
    debugging: bool = True

MAP_OFFSET: Vector = Vector(5,1)

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
        self.testImage: Image = Image('./res/sprites/groun2.png', (215, 123, 186))
        self.selected: Image = Image('./res/sprites/selected.png',)
        self.selected.set_opacity(200)

        self.clock = pygame.time.Clock()
        self.tiles = []

    def update(self):
        self.tiles = []
        self.time_delta = self.clock.tick(60)/1000.0
        self.ui.update(self.time_delta)
        # self.world.update()
        self.add_tiles()
        self.selected_tile_position = self.get_mouse_selected_tile()
        self.mouse.update()
        self.camera.update()
        pygame.display.update()
        
    def get_mouse_selected_tile(self):
        # get the mouse offset position inside the tile
        offset = Vector(self.mouse.position.x % TILE_SIZE.x, self.mouse.position.y % TILE_SIZE.y)
        offset.x += self.camera.position.x % TILE_SIZE.x  # Add camera scroll to offset
        offset.y += self.camera.position.y % TILE_SIZE.y

        # get the cell number
        cell_position = Vector((self.mouse.position.x // TILE_SIZE.x), (self.mouse.position.y // TILE_SIZE.y))
        cell_position.x += int((self.camera.position.x // TILE_SIZE.x))  # Add camera scroll to cell
        cell_position.y += int((self.camera.position.y // TILE_SIZE.y))

        # get the selected cell in iso grid
        selected_pos = Vector(
            (cell_position.y - MAP_OFFSET.y) + (cell_position.x - MAP_OFFSET.x),
            (cell_position.y - MAP_OFFSET.y) - (cell_position.x - MAP_OFFSET.x)
        )
        
        # height and width of a quarter of a tile, select the corner of the tile to nodge to a direction
        h, w = TILE_SIZE.y / 2, TILE_SIZE.x / 2
        if offset.y < (h / w) * (w - offset.x):
            selected_pos.x -= 1
        if offset.y > (h / w) * offset.x + h:
            selected_pos.y += 1
        if offset.y < (h / w) * offset.x - h:
            selected_pos.y -= 1
        if offset.y > (h / w) * (2 * w - offset.x) + h:
            selected_pos.x += 1

        # translate the selected cell to world coordinate
        return Window.to_screen(selected_pos.x, selected_pos.y)

    def add_tiles(self):
        y = 0
        for row in range(0, 5):
            x = 0
            for tile in range(0, 5):
                self.tiles.append(Window.to_screen(x,y))
                x += 1
            y += 1

    def draw(self):
        self.window.display.fill((30, 30, 30))
        # self.world.draw(self.window.display, self.camera.position)
        # self.world.draw_grid(self.window.display, self.camera.position)
        # self.testImage.draw(self.window.display, Vector(60,60), self.camera.position)
 
        for i in self.tiles:
            self.testImage.draw( self.window.display, i, self.camera.position)
        
        self.selected.draw(self.window.display, self.selected_tile_position, self.camera.position)
        self.window.blit_displays()
        self.ui.draw(self.window.screen)

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
                    self.camera.position.x+=10
    
                if event.key == pygame.K_d:
                    self.camera.position.x-=10
              
                if event.key == pygame.K_s:
                    self.camera.position.y-=10
                
                if event.key == pygame.K_w:
                    self.camera.position.y+=10
                    
                    
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
