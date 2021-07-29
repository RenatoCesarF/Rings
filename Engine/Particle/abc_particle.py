import abc

from Engine.Vector import Vector2D

class AbcParticle(abc.ABC):
    def __init__(self,position: Vector2D, velocity: Vector2D, width: int = 1, 
                 height: int = 1, life_time: int = 1, rotation: float = 0, 
                 opacity: int = 255):
        self.position = Vector2D(position.x,position.y)
        self.velocity = Vector2D(velocity.x,velocity.y)
        self.width = int(width)
        self.height = int(height)
        self.rotation = rotation % 360
        self.life_time = life_time *60
        self.opacity = opacity
        self.initial_life_time = self.life_time

    
    def describe(self):
        print("""
            position X: {}
            position Y: {}
            velocity X: {}
            velocity Y: {}
            width: {}
            height: {}
            rotation: {}
            life_time: {}
            opacity: {}
        """.format(self.position.x, self.position.y, self.velocity.x, self.velocity.y, 
                    self.width, self.height, self.rotation, self.life_time, self.opacity))