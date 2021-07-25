import pygame,random
from Engine.Vector import Vector2D

class Particle():
    def __init__(self, x, y, velocity,size, lifeTime = 1, rotation = 0,friction = 0):
        self.position = Vector2D(x,y)
        self.velocity = velocity
        self.friction = friction
        self.size = size
        self.rotation = rotation
        self.lifeTime = lifeTime *60
        self.color = self.randomColor()


    def randomColor(self):
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))


    def Draw(self,surface):
        pygame.draw.circle(surface,self.color,(self.position.x,self.position.y),self.size)
        # pygame.draw.rect(surface,self.color,pygame.Rect((self.position.x,self.position.y), (self.size *2,self.size)),self.size)

    def setParticleImage(self,path):
        pass
  

