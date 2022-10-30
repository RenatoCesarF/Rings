from typing import Any
from Engine.vector import Vector
from Engine.entity import Entity
from Engine.utils import draw_collision_rect
import pygame
from pygame.surface import Surface

from Engine.window import Window

from enum import Enum

class ClickingState(Enum):
    Delete = 1
    Select = 2
    Create = 3

class Mouse(Entity):
    true_position: Vector
    position: Vector
    image: Any  
    left_is_pressed: bool 
    right_is_pressed: bool 
    collision_rect: pygame.Rect
    _state: ClickingState

    def __init__(self, window: Window):
        self._state = ClickingState.Select
        self.window = window
        self.true_position = Vector()
        self.position = Vector()

        self.collision_rect = pygame.Rect(self.position.x, self.position.y, 20, 20)
        self.image = pygame.transform.scale(
            pygame.image.load("res/mouse.png").convert(), (33, 33)
        )
        self.image.set_colorkey((255, 0, 0))
        self.left_is_pressed = False
        self.right_is_pressed = False

    def update(self):
        self.position.x, self.position.y = pygame.mouse.get_pos()
        self.true_position = self.position.copy()
        self.handle_click()
        self.collision_rect.x = self.position.x
        self.collision_rect.y = self.position.y

        self.position = self.transform_mouse_position_to_screen(self.position, self.window.display)
    
    def transform_mouse_position_to_screen(self, position: Vector, display: Surface) -> Vector:
        position.x = int(position.x / (
            self.window.base_screen_size[0] / display.get_width()
        ))
        position.y = int(position.y / (
            self.window.base_screen_size[1] / display.get_height()
        ))
        return position
    
    def handle_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.left_is_pressed = True
        else:
            self.left_is_pressed = False
            
        if pygame.mouse.get_pressed()[2]:
            self.right_is_pressed = True
        else:
            self.right_is_pressed = False
        
    def set_state(self, new_state: ClickingState):
        self._state = new_state 
            
    def draw(self, surface: pygame.Surface, offset: Vector = Vector()) -> None:
        surface.blit(
            self.image,(
                self.true_position.x - self.image.get_width() / 6,
                self.true_position.y - self.image.get_height() / 6,
            ),
        )
        draw_collision_rect(self.collision_rect, surface, offset)

