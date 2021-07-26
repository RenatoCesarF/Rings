import pygame,random
from pygame import gfxdraw
from Engine.Vector import Vector2D
import utils
from enum import Enum

class Shape(Enum):
    Rect = 1
    Box = 2
    Circle = 3
    Polygon = 4



class Particle():
    def __init__(self, x, y, velocity, width = 1, height = 1, lifeTime = 1, rotation = 0,friction = 0, opacity = 255,shape = Shape.Rect):
        self.position = Vector2D(x,y)
        self.velocity = velocity
        self.friction = friction
        self.width = width
        self.height = height
        self.rotation = rotation % 360
        self.lifeTime = lifeTime *60

        self.opacity = opacity

        self.shape = shape

        self.color = (255,255,255)
        self.initialLifeTime = self.lifeTime


    def Draw(self,destinatonSurface):
        formSurface = pygame.Surface((self.width+10,self.height+10),pygame.SRCALPHA)

        #SET SHAPE
        if self.shape == Shape.Rect:
            pygame.draw.rect(formSurface, self.color, pygame.Rect(0, 0, self.width,self.height), width = 0,border_radius = 0)
        elif self.shape == Shape.Box:
            pygame.gfxdraw.box(formSurface,pygame.Rect(0, 0,self.width,self.height),self.color)
        elif self.shape == Shape.Circle:
            pygame.draw.circle(destinatonSurface,self.color,(self.position.x,self.position.y),self.width) #can go directaly to the surface
        elif self.shape == Shape.Polygon:
            #implement polygon
            pygame.draw.circle(destinatonSurface,self.color,(self.position.x,self.position.y),self.width) #can go directaly to the surface
        else:
            pygame.draw.rect(formSurface, self.color, pygame.Rect(0, 0, self.width,self.height), width = 0,border_radius = 2)

        #SET ROTATION
        formSurface, rect= utils.rotate(formSurface,self.rotation,self.position.x,self.position.y)

        #SET OPACITY
        formSurface.set_alpha(self.opacity)

        #ADDING TO SCREEN
        destinatonSurface.blit(formSurface, rect)

    def setParticleImage(self,path):
        pass

    
    def randomColor(self):
        return (random.randint(20,255),random.randint(20,255),random.randint(20,255))
