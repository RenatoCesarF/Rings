import pygame
from Engine.Vector import Vector

class Tile:
    position: Vector
    size: int
    def __init__(self, position: Vector,  size: int):
        self.position = position
        self.size = size

    
    def draw(self, surface: pygame.Surface, offset: Vector, color: tuple = (90,90,90)):
         pygame.draw.rect(surface, color, 
                         pygame.Rect(self.position.x - offset.x,# + self.left_offset.x,
                                     self.position.y - offset.y,# + self.left_offset.y,
                                     self.size,self.size)
         )
