from typing import Any
from Engine.vector import Vector
from Engine.entity import Entity
import pygame

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
    colision_rect: pygame.Rect
    _state: ClickingState

    def __init__(self, window: Window):
        self._state = ClickingState.Select
        self.window = window
        self.true_position = Vector()
        self.position = Vector()

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

        self.position.x -= (
            self.window.screen.get_width() - self.window.base_screen_size[0]
        ) // 3
        self.position.y -= (
            self.window.screen.get_height() - self.window.base_screen_size[1]
        ) // 3

        self.position.x = int(self.position.x / (
            self.window.base_screen_size[0] / self.window.display.get_width()
        ))
        self.position.y = int(self.position.y / (
            self.window.base_screen_size[1] / self.window.display.get_height()
        ))
    
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
