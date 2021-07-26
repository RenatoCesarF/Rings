#TODO: implement image as particle

from typing import Tuple
import pygame,random
from pygame import gfxdraw
from Engine.Vector import Vector2D
import utils
from enum import Enum

class Shape(Enum):
    Rect = 1
    Box = 2
    Circle = 3
    Polygon = 4



class Particle:

    def __init__(self, x, y, velocity, width = 1, height = 1, life_time = 1, rotation = 0, opacity = 100,shape = Shape.Rect):
        """Each particle to be created by a particle emitter

        Args:
            `x` (int): The X position 
            `y` (int): The Y position
            `velocity` (Vector2D): (x,y) velocity of the particle
            `width` (int, optional): The width of the particle's area. Defaults to 1.
            `height` (int, optional): The height of the particle's area. Defaults to 1.
            `life_time` (int, optional): Seconds of existence of this particle. Defaults to 1.
            `rotation` (int, optional): rotation degrees of this particle. Defaults to 0.
            `opacity` (int, optional): Opacity porcentage value  . Defaults to 100.
            `shape` (Shape, optional): The shape of the particle. Defaults to Shape.Rect.
        """
        self.position = Vector2D(x,y)
        self.velocity = velocity
        self.width = width
        self.height = height
        self.rotation = rotation % 360
        self.life_time = life_time *60

        self.opacity = opacity * 100 / 255

        self.shape = shape

        self.color = (255,255,255)
        self.initial_life_time = self.life_time


    def Draw(self,destinatonSurface) -> None:
        formSurface = pygame.Surface((self.width+10,self.height+10),pygame.SRCALPHA)

        #SET SHAPE
        if self.shape == Shape.Rect:
            pygame.draw.rect(formSurface, self.color, pygame.Rect(0, 0, self.width,self.height), width = 0,border_radius = 0)
        elif self.shape == Shape.Box:
            pygame.gfxdraw.box(formSurface,pygame.Rect(0, 0,self.width,self.height),self.color)
        elif self.shape == Shape.Circle:
            pygame.draw.circle(destinatonSurface,self.color,(self.position.x,self.position.y),self.width) #can go directaly to the surface
        elif self.shape == Shape.Polygon:
            #implement polygon
            pygame.draw.circle(destinatonSurface,self.color,(self.position.x,self.position.y),self.width) #can go directaly to the surface
        else:
            pygame.draw.rect(formSurface, self.color, pygame.Rect(0, 0, self.width,self.height), width = 0,border_radius = 2)

        #SET ROTATION
        formSurface, rect= utils.rotate(formSurface,self.rotation,self.position.x,self.position.y)

        #SET OPACITY
        formSurface.set_alpha(self.opacity)

        #ADDING TO SCREEN
        destinatonSurface.blit(formSurface, rect)

    def set_particle_image(self,path) -> None:
        pass

    
    def random_color(self) -> Tuple:
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))
