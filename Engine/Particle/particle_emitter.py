# TODO: implement oneshot logic
# TODO: improve random velocity with noise

import pygame
from random import randint, uniform
from typing import Tuple

from Engine.Particle.shape_particle import ShapeParticle
from Engine.Particle.abc_particle import AbcParticle
from Engine.Particle.image_particle import ImageParticle
from Engine.vector import Vector
from Engine.Glow import Glow


class ParticleEmitter(object):
    def __init__(
        self,
        position: Vector,
        amount: int,
        particle_pattern: AbcParticle,
        oneShot: bool = False,
        emittion_height: float = 0,
        emittion_width: float = 0,
        velocity_RC: Tuple = [],
        size_RC: Tuple = [],
    ):
        """It Emmit particles based in a particle_pattern at a determinated position\n
        Args:
            `position` (Vector): Initial Position of emittion
            `amount` (int): Amount of particles that gonna be generated
            `particle_pattern` (Particle): A base particle used as pattern that
            gonna be emitted
            `oneShot` (bool, optional): If it's one shot or not. If yes the
            emittion start and stop immediately. Defaults to False.
            `emittion_height` (float, optional): the height of the emittion,
            `emittion_width` (float, optional): the width of the emittion,
            `velocity_RC` (Vector, optional): The Random Coeficient of velocity
            applied to the particle each emmition. Defaults to Vector(1,1).
            `size_RC` (Vector, optional): The Random Coeficient of sized applied
            to the particle each emmition. Defaults to Vector(1,1).

        - The emittion_height and emittion_width change the size of the emittion shape.
        the increasing of those values will add to the position, not from the middle but from
        the top-left corner
        """
        self.oneShot = oneShot
        self.isEmitting = True
        self.position = position
        self.amount = amount
        self.particle_pattern = particle_pattern
        self.velocity_RC = velocity_RC
        self.size_RC = size_RC
        self.initial_update_cicle = self.update_cicle = (
            particle_pattern.life_time / amount
        )
        self.particles = []
        self.emittion_height = emittion_height
        self.emittion_width = emittion_width

    def update(self, surface, timestep=1):
        """Update every single particle of the list and draw each in the surface passed"""
        if self.isEmitting and not self.is_emitter_full():
            self.update_cicle -= timestep
            # if self.oneShot:
            #     self.isEmitting = False
            # m    self.fill_particle_list()

            if self.update_cicle <= 0:
                self.update_cicle = self.initial_update_cicle
                self.add_particle()

        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.life_time -= timestep

            particle.position.add(particle.velocity)
            particle.rotation += uniform(1, 10)
            particle.draw(
                surface, Glow(width=40, height=40, radius=100, color=(20, 20, 60, 110))
            )

            if particle.life_time <= 0:
                self.particles.pop(i)

    def fill_particle_list(self):
        if self.is_emitter_full():
            return

        for i in range(0, self.amount):
            self.add_particle()

    def add_particle(self):
        """Add one particle to the list based in the particle_pattern passed
        in cosntructor
        """
        pp = self.particle_pattern

        if type(self.particle_pattern) == ShapeParticle:
            p = ShapeParticle(
                position=self.position,
                velocity=Vector(pp.velocity.x, pp.velocity.y),
                width=randint(pp.width - 2, pp.width + 2),  # randint(11,10),
                height=randint(pp.height - 2, pp.height + 2),
                life_time=pp.life_time / 60,
                shape=pp.shape,
            )
            self.particles.append(p)
            return

        p = ImageParticle(
            pp.image,
            position=self.get_random_position_in_array(),
            velocity=Vector(pp.velocity.x, pp.velocity.y),
            width=randint(pp.width - 5, pp.width + 5),  # randint(11,10),
            height=randint(pp.height - 5, pp.height + 5),
            life_time=pp.life_time / 60,
        )
        self.particles.append(p)

    def get_random_position_in_array(self) -> Vector:
        if self.emittion_width == 0 and self.emittion_height == 0:
            return self.position

        randomY = uniform(self.position.y, self.position.y + self.emittion_height)
        randomX = uniform(self.position.x, self.position.x + self.emittion_width)
        return Vector(randomX, randomY)

    def update_emitter_position(self, newPosition: Vector):
        self.position = newPosition

    def stop(self):
        self.isEmitting = False

    def start(self):
        self.isEmitting = True

    def is_emitter_full(self) -> bool:
        return len(self.particles) >= self.amount
