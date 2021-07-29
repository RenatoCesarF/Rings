#TODO: implement shape emission
#TODO: implement oneshot logic
#TODO: improve emission logic

from random import randint, uniform

from Engine.Particle.shape_particle import ShapeParticle
from Engine.Particle.abc_particle import AbcParticle
from Engine.Particle.image_particle import ImageParticle
from Engine.Vector import Vector2D

class ParticleEmitter(object):
    def __init__(self,position: Vector2D, amount: int, particle_pattern: AbcParticle,
                 oneShot: bool = False, velocity_RC: Vector2D = Vector2D(1,1),
                 size_RC: Vector2D = Vector2D(1,1)):
        """It Emmit particles based in a particle_pattern at a determinated position\n
        Args:
            `position` (Vector2D): Initial Position of emittion
            `amount` (int): Amount of particles that gonna be generated
            `particle_pattern` (Particle): A base particle used as pattern that 
            gonna be emitted
            `oneShot` (bool, optional): If it's one shot or not. If yes the 
            emittion start and stop immediately. Defaults to False.
            `velocity_RC` (Vector2D, optional): The Random Coeficient of velocity
            applied to the particle each emmition. Defaults to Vector2D(1,1).
            `size_RC` (Vector2D, optional): The Random Coeficient of sized applied 
            to the particle each emmition. Defaults to Vector2D(1,1).
        """
        self.oneShot = oneShot
        self.isEmitting = True
        self.position =position
        self.amount = amount
        self.particle_pattern = particle_pattern
        self.velocity_RC = velocity_RC
        self.size_RC = size_RC
        self.initial_update_cicle = self.update_cicle = particle_pattern.life_time/amount
        self.particles = []
     
    def update(self,surface,timestep = 1):
        """Update every single particle of the list and draw each in the surface passed"""
        if self.isEmitting:
            self.update_cicle -= timestep
            if self.oneShot:
                self.isEmitting = False
                self.fill_particle_list()
        
            if  self.update_cicle <= 0:
                self.update_cicle = self.initial_update_cicle
                self.add_particle()
                
        i = 0
        while i < len(self.particles):
            p = self.particles[i]
            p.life_time -= timestep
         
            p.position.add(p.velocity)
            p.rotation += uniform(1,3)
            p.Draw(surface)

            if p.life_time <= 0:
                self.particles.pop(i)
            else:
                i += 1
     
    def fill_particle_list(self): 
        if self.is_emitter_full():
            return
        
        for i in range(0,self.amount):
            self.add_particle()

    def add_particle(self):
        """Add one particle to the list based in the particle_pattern passed 
           in cosntructor
        """
        pp = self.particle_pattern
        
        if type(self.particle_pattern) == ShapeParticle:
            p = ShapeParticle(
                position = self.position,
                velocity = Vector2D(randint(2,10),randint(3,10)/10 - 1),
                width = randint(pp.width - 10, pp.width +10),# randint(11,10),
                height = randint(pp.height-5, pp.height+5),
                life_time = pp.life_time/60,
                rotation = 90,
                shape = pp.shape,
            )
            self.particles.append(p)
            return
        
        p = ImageParticle(
            "",
            position = self.position,
            velocity = Vector2D(randint(2,10),randint(3,10)/10 - 1),
            width = randint(pp.width - 10, pp.width +10),# randint(11,10),
            height = randint(pp.height-5, pp.height+5),
            life_time = pp.life_time/60,
            rotation = 90
            
        )
    
    def update_emitter_position(self, newPosition):
        self.position = newPosition

    def stop(self):
        self.isEmitting = False
        
    def start(self):
        self.isEmitting = True

    def is_emitter_full(self) -> bool:
        return len(self.particles) >= self.amount
        