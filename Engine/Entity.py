import pygame
from Engine.Vector import Vector2D

class Entity(object):
    def __init__(self, image_path: str,position: pygame.Vector2D, height: float, width: float) -> None:
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.position = position
    
    def draw(self,surface: pygame.Surface, camera_offset: float) -> None:
        surface.blit(self.image)
        pass

    def update(self) -> None:
        pass