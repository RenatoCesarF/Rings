#TODO: implement image as particle

from typing import Tuple
from enum import Enum
import random

import pygame

from Engine import utils
from Engine.Vector import Vector2D

class Shape(Enum):
    Rect = 1
    Box = 2
    Circle = 3
    Polygon = 4

class Particle(object):
    def __init__(self, x: float, y: float, velocity: Vector2D, width: float = 1, 
                 height: float = 1, life_time: int = 1, rotation: float = 0, 
                 opacity: int = 255,shape: Shape = Shape.Rect):
        """Each particle to be created by a particle emitter\n
        Args:
            `x` (float): The X position 
            `y` (float): The Y position
            `velocity` (Vector2D): (x,y) velocity of the particle
            `width` (float, optional): The width of the particle's area. Defaults to 1.
            `height` (float, optional): The height of the particle's area. Defaults to 1.
            `life_time` (int, optional): Seconds of existence of this particle. Defaults to 1.
            `rotation` (int, optional): rotation degrees of this particle. Defaults to 0.
            `opacity` (int, optional): Opacity of the particle, it's from 0 to 255 value  . Defaults to 255.
            `shape` (Shape, optional): The shape of the particle. Defaults to Shape.Rect.
        """
        self.position = Vector2D(x,y)
        self.velocity = velocity
        self.width = width
        self.height = height
        self.rotation = rotation % 360
        self.life_time = life_time *60
        self.opacity = opacity
        self.shape = shape

        self.color = (255,255,255)
        self.initial_life_time = self.life_time

    @classmethod
    def fromImage(cls, path):
        print("CRIOU PELA IMAGEM")
        return cls()

    def Draw(self,destinatonSurface) -> None:
        formSurface = pygame.Surface((self.width+10,self.height+10),pygame.SRCALPHA)

        #SET SHAPE
        if self.shape == Shape.Rect:
            pygame.draw.rect(formSurface, self.color, 
                             pygame.Rect(0, 0, self.width,self.height), 
                             width = 0,border_radius = 0)
        elif self.shape == Shape.Box:
            pygame.gfxdraw.box(formSurface,pygame.Rect(0, 0,self.width,self.height),
                                self.color)
        elif self.shape == Shape.Circle:
            pygame.draw.circle(destinatonSurface,self.color,
                               (self.position.x,self.position.y),self.width) #can go directaly to the surface
        elif self.shape == Shape.Polygon:
            #implement polygon
            pygame.draw.circle(destinatonSurface,self.color,
                                (self.position.x,self.position.y),self.width)
        else:
            pygame.draw.rect(formSurface, self.color, 
                             pygame.Rect(0, 0, self.width,self.height), width = 0,border_radius = 2)

        #SET ROTATION
        formSurface, rect= utils.rotate(formSurface,self.rotation,
                                        self.position.x,self.position.y)

        #SET OPACITY
        formSurface.set_alpha(self.opacity)

        #ADDING TO SCREEN
        destinatonSurface.blit(formSurface, rect)

    def random_color(self) -> Tuple:
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))
