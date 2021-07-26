import pygame,random
from Engine.Vector import Vector2D
import utils

class Particle():
    def __init__(self, x, y, velocity,size, lifeTime = 1, rotation = 0,friction = 0):
        self.position = Vector2D(x,y)
        self.velocity = velocity
        self.friction = friction
        self.size = size
        self.rotation = rotation % 360
        self.lifeTime = lifeTime *60
        self.initialLifeTime = self.lifeTime
        self.color = (255,255,255)


    def randomColor(self):
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))


    def Draw(self,surface):
        if not self.rotation:
            pygame.draw.circle(surface,self.color,(self.position.x,self.position.y),self.size)
            # pygame.draw.rect(surface,self.color,pygame.Rect((self.position.x,self.position.y), (self.size *2,self.size)),self.size)
            return

        square = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        square.fill(self.color)

        square, rect= utils.rotate(square,self.rotation,self.position.x,self.position.y)

        surface.blit(square, rect)

    def setParticleImage(self,path):
        pass
  

