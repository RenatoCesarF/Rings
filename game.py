from __future__ import annotations

from typing import Dict, List,Any, Tuple

import math 
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

class Bullet(Entity):
    position: Vector
    target: Entity
    direction: Vector
    speed: float
    alive: bool
    collision_rect: Rect
    def __init__(self, position: Vector, target: Entity, speed: float = 1):
        self.position = position
        self.target = target
        self.direction = Vector()
        self.speed = speed
        self.alive = True
        self.collision_rect = Rect(position.x, position.y, 5, 5)
    def update(self):
        if not self.target or not self.alive:
            return
        self.direction.x = self.target.position.x - self.position.x
        self.direction.y = self.target.position.y - self.position.y 

        self.direction = self.direction.normalize()
        self.position.x +=  self.direction.x * self.speed
        self.position.y +=  self.direction.y * self.speed
        self.collision_rect.x = self.position.x - 2
        self.collision_rect.y = self.position.y - 2

        if not self.target.collision_rect or self.target.collision_rect is None:
            return
        
        self.handle_target_collision()

    def handle_target_collision(self):
        if not self.collided_with_target():
            return
        self.alive = False

    
    def collided_with_target(self):
        if self.collision_rect.colliderect(self.target.collision_rect):
            return True
        return False

        
    def draw(self, surface: Surface, offset: Vector):
        if not self.target or not self.alive:
            return
        pygame.draw.circle(
            surface, 
            (200,0,0),
            (self.position.x - offset.x, self.position.y - offset.y),
            2
        )
        # draw_collision_rect(self.collision_rect, surface, offset)


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

    def __init__(self) -> None:
        self.unit_manager = UnitManager(self)
        self.running = True
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
        self.bullets: List[Bullet] = []

    def update(self):
        self.time_delta = self.clock.tick(60)/1000.0
    
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
        
        if self.unit_manager.selected_unit:
            self.selected_tile_position = self.unit_manager.selected_unit.tile_position
            if self.mouse.right_is_pressed:
                self.unit_manager.remove(self.unit_manager.selected_unit)
                
        if self.mouse.left_is_pressed and not self.unit_manager.selected_unit:
            self.add_unit_in_tile()
            
        
        self.mouse.update()
        for i, b in enumerate(self.bullets):
            if not b.alive:
                self.bullets.pop(i)
            b.update()
        
            
        self.camera.update()
        pygame.display.update()
        
    def add_unit_in_tile(self):
        if not self.world.is_tile_position_valid(
                self.selected_tile_position.x,
                self.selected_tile_position.y
            ):
            return
        
        self.unit_manager.add_unit_to_list(
            Unit(Vector(self.selected_tile_position.x,self.selected_tile_position.y))
        )

    def draw(self):
        self.window.display.fill((80, 90, 90))
        self.world.draw(self.window.display, self.camera.position)

        self.draw_selection_square(self.window.display)

        self.unit_manager.draw(self.window.display, self.camera.position)

        for b in self.bullets:
            b.draw(self.window.display, self.camera.position)
        self.window.blit_displays()
        self.ui.draw(self.window.screen)
        # self.ui.write(str(int(self.clock.get_fps())), Vector(0,10))
    
        # self.ui.write("Selected Tile: "  + str(self.selected_tile_position.to_tuple), Vector(0,30))
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

                if event.key == pygame.K_SPACE:
                    target = self.unit_manager.selected_unit
                    if not target:
                        return
                    self.bullets.append(
                        Bullet(Vector(0,0),target, 4)
                    )

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
