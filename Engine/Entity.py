import pygame
from Engine.Vector import Vector


class Entity:
    def __init__(
        self, image_path: str, position: pygame.Vector, height: float, width: float
    ) -> None:
        self.image = pygame.image.load(image_path).convert()
        self.position = position

    def draw(self, surface: pygame.Surface, camera_offset: float) -> None:
        surface.blit(self.image)
        pass

    def update(self) -> None:
        pass
