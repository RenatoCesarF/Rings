
import pygame,random
from Engine.Vector import Vector2D

class Particle():
    def __init__(self,position_x, position_y, size, velocity_x,velocity_y, lifeTime):
        self.position = Vector2D(position_x,position_y)
        self.velocity = Vector2D(velocity_x,velocity_y)
        self.size = size
        self.lifeTime = lifeTime *60
        self.color = self.randomColor()


    def randomColor(self):
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))


    def Draw(self,surface):
        pygame.draw.circle(surface,self.color,(self.position.x,self.position.y),self.size)

    def Update(self):
        self.lifeTime -= 1

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        self.velocity.y +=0.08


      

 
