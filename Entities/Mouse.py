from typing import Any
from enum import Enum

import pygame
from pygame.surface import Surface

from Engine.Vector import Vector
from Engine.Entity import Entity

# from Engine.utils import draw_collision_rect
from Engine.image import Image

from Engine.Window import Window


class ClickingState(Enum):
    """An enum to represent the possible mouse state"""
    Delete = 1
    Select = 2
    Create = 3


class Mouse(Entity):
    """The class that represents the mouse entity in the game"""

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
        self.true_position = Vector.zero()
        self.position = Vector.zero()

        self.image = Image('res/mouse.png', (255, 0, 0))
        self.image.scale_to_resolution((43, 43))

        self.collision_rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.image.width,
            self.image.height,
        )

        self.left_is_pressed = False
        self.right_is_pressed = False

        super().__init__(
            self.position, (self.image.width, self.image.height), name='Mouse'
        )

    def update(self):
        self.position.x, self.position.y = pygame.mouse.get_pos()
        self.true_position = self.position.copy()
        self.handle_click()

        self.collision_rect.x = self.position.x - self.image.width / 2
        self.collision_rect.y = self.position.y - self.image.height / 2

        self.position = self.transform_mouse_position_to_screen(
            self.position, self.window.display
        )

    def transform_mouse_position_to_screen(
        self, position: Vector, display: Surface
    ) -> Vector:
        position.x = int(
            position.x
            / (self.window.base_screen_size[0] / display.get_width())
        )
        position.y = int(
            position.y
            / (self.window.base_screen_size[1] / display.get_height())
        )
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
        """Change the mouse state, its action"""
        self._state = new_state

    def draw(self, surface: pygame.Surface, offset: Vector = Vector.zero()):
        pos = Vector(
            self.true_position.x - self.image.width / 6,
            self.true_position.y - self.image.height / 6,
        )
        self.image.draw(surface, pos, offset)

        # self.collision_rect.draw_collision_rect(self.collision_rect, surface, offset)

    def get_state(self) -> str:
        """
        Return the action that the mouse state is doing
        """
        return str(self._state)
