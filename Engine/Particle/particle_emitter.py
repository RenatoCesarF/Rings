from enum import Enum

from pygame.display import update
from Engine.Particle.particle import Particle
from Engine.Vector import Vector2D
from random import randint, uniform
import utils

class ParticleEmitter():
    def __init__(self,position, amount,particlePattern, oneShot=False,velocity_RC = Vector2D(1,1),size_RC = Vector2D(1,1)):
        self.oneShot = oneShot
        self.isEmitting = True
        self.position =position
        self.amount = amount
        self.particlePattern = particlePattern
        self.velocity_RC = velocity_RC
        self.size_RC = size_RC
        self.initialUpdateCicle = self.updateCicle = self.particlePattern.lifeTime/ self.amount

        self.particles = []

            

    def fillParticleList(self):
        for i in range(0,self.amount):
            self.addParticle()


    def update(self,surface):
        if self.isEmitting:
            self.updateCicle -=1
            if  self.updateCicle <= 0:
                self.addParticle()
                self.updateCicle = self.initialUpdateCicle

        i=0
        while i < len(self.particles):
            p = self.particles[i]
            p.lifeTime -= 1
            if not p.position.y >=399:
                p.position.add(p.velocity)
                p.rotation +=uniform(1,3)

            p.Draw(surface)


            if p.lifeTime <=0:
                self.particles.pop(i)
            else:               
                i += 1


    def addParticle(self):
        pp =  self.particlePattern
        p = Particle(
            x = self.position.x,
            y = self.position.y,
            velocity = Vector2D(randint(0,20)/10 - 1,randint(2,4)),
            width = pp.width,# randint(11,10),
            height = pp.height,#randint(11,10),
            lifeTime = pp.lifeTime/60,
            shape = pp.shape,
            rotation = 90
        )
        p.friction = 0.06
        self.particles.append(p)

    def stop(self):
        self.isEmitting = False
        
    def start(self):
        self.isEmitting = True

    def updateEmitterPosition(self, newPosition):
        self.position = newPosition
