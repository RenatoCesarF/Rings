from Engine.Entity import Entity
from Engine.Vector import Vector


class Camera(Entity):
    _target: Entity
    window_size: tuple
    position: Vector

    def __init__(self, target: Entity, window_size: tuple):
        self._target = target
        self.position = Vector()
        self.window_size = window_size

    def update(self):
        self.position.x = self._target.position.x - self.window_size[0] / 2
        self.position.y = self._target.position.y - self.window_size[1] / 2

    def draw(self, surface, offset):
        pass

    def set_target(self, _target: Entity):
        self._target = _target
