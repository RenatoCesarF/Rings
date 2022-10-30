# TODO: add animation to the image using list of images or an animation Object
from typing import Tuple
from abc import ABC
import abc

import random

import pygame
from pygame.surface import Surface
from Engine import utils
from Engine.vector import Vector
from Engine.shape import Shape
from Engine.Particle.abc_particle import AbcParticle


class ImageParticle(AbcParticle):
    def __init__(
        self,
        image: Surface,
        position: Vector,
        velocity: Vector,
        life_time: float = 1,
        opacity: int = 255,
        scale: float = 1,
    ):
        """Each particle to be created by a particle emitter\n
        Args:
            `image` (Surface): The image already loaded
            `position` (Vector): The X and Y position
            `velocity` (Vector): (x,y) velocity of the particle
            `life_time` (float, optional): Seconds of existence of this particle. Defaults to 1.
            `opacity` (int, optional): Opacity of the particle, it's from 0 to 255 value  . Defaults to 255.
            `scale` (float, optional): The scale factory of the image. Defaults to 1
        """
        self.scale = scale
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image, (self.width * scale, self.height * scale)
        )
        super().__init__(
            position, velocity, self.width, self.height, life_time, opacity
        )

    def draw(self, destinatonSurface) -> None:
        """Draws the particle into the destination surface after set it's opacity

        Args:
            destinatonSurface (pygame.Surface): The surface where ther particle will be blited at
        """
        self.image.set_alpha(self.opacity)
        destinatonSurface.blit(self.image, self.position.copy())

        # TODO: make rotations

    def __str__(self):
        desc = super().__str__()
        desc += f"""
            scale: {self.scale}
            image: {self.image}
        """
        return desc
