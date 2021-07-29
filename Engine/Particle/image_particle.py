#TODO: implement image as particle

from typing import Tuple
from abc import ABC
import abc

import random

import pygame

from Engine import utils
from Engine.Vector import Vector2D
from Engine.shape import Shape
from Engine.Particle.abc_particle import AbcParticle

class ImageParticle(AbcParticle):
    def __init__(self,path: str, position: Vector2D, velocity: Vector2D, width: int = 1, 
                 height: int = 1, life_time: int = 1, rotation: float = 0, 
                 opacity: int = 255):
        """Each particle to be created by a particle emitter\n
        Args:
            `path` (str): The path to the image source
            `x` (float): The X position 
            `y` (float): The Y position
            `velocity` (Vector2D): (x,y) velocity of the particle
            `width` (int, optional): The width of the particle's area. Defaults to 1.
            `height` (int, optional): The height of the particle's area. Defaults to 1.
            `life_time` (int, optional): Seconds of existence of this particle. Defaults to 1.
            `rotation` (int, optional): rotation degrees of this particle. Defaults to 0.
            `opacity` (int, optional): Opacity of the particle, it's from 0 to 255 value  . Defaults to 255.
        """
        super().__init__(position,velocity,width,height,life_time,rotation,opacity)

        self.path = path


    def Draw(self,destinatonSurface) -> None:
        formSurface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)

        #SET ROTATION
        formSurface, rect= utils.rotate(formSurface,self.rotation,
                                        self.position.x,self.position.y)

        #SET OPACITY
        formSurface.set_alpha(self.opacity)

        #ADDING TO SCREEN
        destinatonSurface.blit(formSurface, rect)

