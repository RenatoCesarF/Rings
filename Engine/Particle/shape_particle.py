from typing import List, Tuple
import random
import pygame

from Engine import utils
from Engine.Vector import Vector
from Engine.shape import Shape
from Engine.Particle.abc_particle import AbcParticle
from Engine.Glow import Glow


class ShapeParticle(AbcParticle):
    def __init__(
        self,
        position: Vector,
        velocity: Vector,
        width: int = 1,
        height: int = 1,
        life_time: float = 1,
        color: Tuple = (255, 255, 255),
        opacity: int = 255,
        rotation: float = 0,
        shape: Shape = Shape.Rect,
    ):
        """Each particle to be created by a particle emitter\n
        Args:
            `position` (Vector): Position.
            `velocity` (Vector): (x,y) velocity of the particle
            `width` (int, optional): The width of the particle's area. Defaults to 1.
            `height` (int, optional): The height of the particle's area. Defaults to 1.
            `life_time` (float, optional): Seconds of existence of this particle. Defaults to 1.
            `color` (tuple, optional): Particle color.
            `opacity` (int, optional): Opacity of the particle, it's from 0 to 255 value  . Defaults to 255.
            `rotation` (int, optional): rotation degrees of this particle. Defaults to 0.
            `shape` (Shape, optional): The shape of the particle. Defaults to Shape.Rect.
        """
        super().__init__(
            position, velocity, width, height, life_time, opacity, rotation
        )

        self.color = color
        self.shape = shape

    def set_polygon_points(self, points: List) -> None:
        self.points = points

    def draw(
        self, destinatonSurface: pygame.Surface, glow: Glow = None
    ) -> None:
        formSurface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )

        # SET SHAPE
        if self.shape == Shape.Rect:
            pygame.draw.rect(
                formSurface,
                self.color,
                pygame.Rect(0, 0, self.width, self.height),
                width=0,
                border_radius=0,
            )
        elif self.shape == Shape.Box:
            pygame.gfxdraw.box(
                formSurface,
                pygame.Rect(0, 0, self.width, self.height),
                self.color,
            )
        elif self.shape == Shape.Circle:
            pygame.draw.circle(
                destinatonSurface,
                self.color,
                (self.position.x, self.position.y),
                self.width,
            )  # can go directaly to the surface
        elif self.shape == Shape.Polygon:
            pygame.draw.polygon(
                destinatonSurface, self.color, self.points, self.width
            )
        else:
            pygame.draw.rect(
                formSurface,
                self.color,
                pygame.Rect(0, 0, self.width, self.height),
                width=0,
                border_radius=2,
            )

        # SET ROTATION
        formSurface, rect = utils.rotate(
            formSurface, self.rotation, self.position.x, self.position.y
        )

        # SET OPACITY
        formSurface.set_alpha(self.opacity)

        # ADDING TO SCREEN
        destinatonSurface.blit(formSurface, rect)

        if glow == None:
            return

        destinatonSurface.blit(
            glow.circle_glow(),
            (self.position.x - glow.width, self.position.y - glow.height),
            special_flags=pygame.BLEND_RGB_ADD,
        )

    def random_color(self) -> Tuple:
        return (
            random.randint(20, 255),
            random.randint(20, 255),
            random.randint(20, 255),
        )

    def __str__(self):
        desc = super().__str__()
        desc += f"""
            color: {self.color}
            shape: {self.shape}
        """
        return desc
