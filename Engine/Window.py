from typing import List, Tuple
import pygame

from Engine.vector import Vector
from Engine.config import TILE_SIZE

MAP_OFFSET: Vector = Vector(5, 1)


class Window:
    screen: pygame.Surface
    screen_real_size: Tuple[int, int]
    base_screen_size: Tuple[int, int]
    display: pygame.Surface

    def __init__(self, resolution: List[int], is_mouse_visible: bool = False):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(32)
        pygame.display.set_caption("Rings")
        pygame.mouse.set_visible(is_mouse_visible)
        self.base_screen_size = (resolution[0], resolution[1])
        self.screen_real_size = (600, 400)

        self.screen = pygame.display.set_mode(  # type: ignore
            (self.base_screen_size[0], self.base_screen_size[1]), 0, 32
        )

        self.display = pygame.Surface((300, 200))

    def blit_displays(self):
        self.screen.blit(
            pygame.transform.scale(self.display, self.base_screen_size),
            (
                (self.screen.get_width() - self.base_screen_size[0]) // 2,
                (self.screen.get_height() - self.base_screen_size[1]) // 2,
            ),
        )

    @staticmethod
    def to_isometric_position_from_vector(position: Vector) -> Vector:
        return Window.to_isometric_position(position.x, position.y)

    @staticmethod
    def to_isometric_position(x: int, y: int) -> Vector:
        screen_x = (MAP_OFFSET.x * TILE_SIZE.x) + (x - y) * (TILE_SIZE.x / 2)
        screen_y = (MAP_OFFSET.y * TILE_SIZE.y) + (x + y) * (TILE_SIZE.y / 2)
        return Vector(int(screen_x), int(screen_y))
