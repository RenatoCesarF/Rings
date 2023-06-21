from turtle import onclick
from typing import Any, List, Tuple, Union, Callable

from pygame.surface import Surface
import pygame
from pygame.font import Font
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from Engine import utils
from Engine.vector import Vector


class PopUpInfo:
    def __init__(self):
        pass


class DisplayPanel:
    def __init__(self):
        pass


class Button:
    on_click: Callable
    ui_button: UIButton

    def __init__(self, ui_button: UIButton, on_click: Callable):
        self.on_click = on_click
        self.ui_button = ui_button


class UI:
    manager: UIManager
    buttons: List[Button]
    font: Font
    surface: Surface

    def __init__(self, window_size: Tuple[int, int], theme_path: str, surface: Surface):
        self.manager = pygame_gui.UIManager(window_size, theme_path)
        self.font = pygame.font.Font("res/Pixellari.ttf", 22)
        self.surface = surface
        self.buttons = []

    def add_button(self, position: Tuple[int, int], text: str, on_click):
        self.buttons.append(Button(self._create_button(position, text), on_click))

    def check_events(self, event):
        for button in self.buttons:
            if event.ui_element == button.ui_button:
                button.on_click()

    def _create_button(self, position: Tuple[int, int], text: str):
        return pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (-1, -1)),
            text=text,
            manager=self.manager,
        )

    def write(self, text: str, position: Vector = Vector(10, 10)) -> None:
        utils.draw_text(
            self.font,
            text,
            self.surface,
            position,
        )

    def update(self, delta_time: float):
        self.manager.update(delta_time)

    def draw(self, surface: Surface):
        self.manager.draw_ui(surface)
