#TODO: implement shape emission
#TODO: implement oneshot logic
#TODO: improve emission logic

from Engine.Particle.particle import Particle
from Engine.Vector import Vector2D
from random import randint, uniform

class ParticleEmitter:
    def __init__(self,position, amount,particle_pattern, oneShot=False,velocity_RC = Vector2D(1,1),size_RC = Vector2D(1,1)):
        
        '''        
        It Emmit particles based in a particle_pattern at a determinated position \n

        :param `position`: The amount of distance traveled
        :type position: Vector2D

        :param `amount`: 
        :type amount: int

        :param `particle_pattern`: A particle sample of how the particles of this emitter gonna be
        :raises: :class:`RuntimeError`: Out of fuel

        '''

        self.oneShot = oneShot
        self.isEmitting = True
        self.position =position
        self.amount = amount
        self.particle_pattern = particle_pattern
        self.velocity_RC = velocity_RC
        self.size_RC = size_RC
        self.initial_update_cicle = self.update_cicle = self.particle_pattern.life_time/ self.amount

        self.particles = []
     
    def update(self,surface):
        """Update every single particle of the list and draw each in the surface passed"""
        if self.isEmitting:
            self.update_cicle -=1
            if  self.update_cicle <= 0:
                self.add_particle()
                self.update_cicle = self.initial_update_cicle

        i=0
        while i < len(self.particles):
            p = self.particles[i]
            p.life_time -= 1
            if not p.position.y >=399:
                p.position.add(p.velocity)
                p.rotation +=uniform(1,3)

            p.Draw(surface)


            if p.life_time <=0:
                self.particles.pop(i)
            else:               
                i += 1

    def add_particle(self):
        """
            Add one particle to the list based in 
            the particle_pattern passed in cosntructor"""
        pp =  self.particle_pattern
        p = Particle(
            x = self.position.x,
            y = self.position.y,
            velocity = Vector2D(randint(0,20)/10 - 1,randint(2,4)),
            width = pp.width,# randint(11,10),
            height = pp.height,#randint(11,10),
            life_time = pp.life_time/60,
            shape = pp.shape,
            rotation = 90
        )
        self.particles.append(p)

    def update_emitter_position(self, newPosition):
        self.position = newPosition

    def fill_particle_list(self):
        for i in range(0,self.amount):
            self.add_particle()

    def stop(self):
        self.isEmitting = False
        
    def start(self):
        self.isEmitting = True
