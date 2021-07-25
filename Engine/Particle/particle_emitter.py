from enum import Enum
from Engine.Particle.particle import Particle
from Engine.Vector import Vector2D
from random import randint 
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
        self.particles = []

    def fillParticleList(self):
        for i in range(0,self.amount):
            self.addParticle()


    def update(self,surface):
     
        i=0
        while i < len(self.particles):
            self.particles[i].lifeTime -= 1
            self.particles[i].position.add(self.particles[i].velocity)

            self.particles[i].Draw(surface)

            if self.particles[i].lifeTime <= 0:
                self.particles.pop(i)
            else:               
                i += 1
           

            


    def stop(self):
        self.isEmitting = False
        
    def start(self):
        self.isEmitting = True

    def getVectorUsingRC(self,startVector,rcVector):
        return Vector2D()
        

    def addParticle(self):
        pp =  self.particlePattern
        p = Particle(
            self.position.x, self.position.y,
            Vector2D(randint(0,10)/10 - 1,-randint(0,5)),
            randint(6,20),
            pp.lifeTime/60,
        )
        p.friction = 0.06
        self.particles.append(p)

    def updateEmitterPosition(self, newPosition):
        self.position = newPosition
