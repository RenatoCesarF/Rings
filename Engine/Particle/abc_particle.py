import abc

from Engine.vector import Vector


class AbcParticle(abc.ABC):
    def __init__(
        self,
        position: Vector,
        velocity: Vector,
        width: int = 1,
        height: int = 1,
        life_time: float = 1,
        opacity: int = 255,
        rotation: float = 0,
    ):
        self.position = Vector(position.x, position.y)
        self.velocity = Vector(velocity.x, velocity.y)
        self.width = int(width)
        self.height = int(height)
        self.rotation = rotation % 360
        self.life_time = life_time * 60
        self.opacity = opacity
        self.initial_life_time = self.life_time

    def __str__(self):
        return f"""
        position X: {self.position.x}
        position Y: {self.position.y}
        velocity X: {self.velocity.x}
        velocity Y: {self.velocity.y}
        width: {self.width}
        height: {self.height}
        rotation: {self.rotation}
        life_time: {self.life_time}
        opacity: {self.opacity}
        """
