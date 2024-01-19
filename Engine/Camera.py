from random import randint
from typing import Tuple


from Engine.Entity import Entity
from Engine.Vector import Vector


class Camera(Entity):
    _target: Entity
    window_size: Tuple[int, int]
    position: Vector
    shaking_amount: Vector
    current_shake_rate: int
    original_shake_rate: int
    is_shaking: bool
    shaking_timer: int

    def __init__(self, target: Entity, window_size: Tuple[int, int]):
        self._target = target
        self.position = Vector.zero()
        self.current_shake_rate = 0
        self.original_shake_rate = 0
        self.shaking_amount = Vector.zero()
        self.is_shaking = False
        self.window_size = window_size
        self.shaking_timer = 0

    def update(self):
        if (
            self._target
            and hasattr(self._target, 'position')
            and hasattr(self._target.position, 'x')
        ):
            self.position.x = int(
                self._target.position.x - self.window_size[0] / 2
            )
            self.position.y = int(
                self._target.position.y - self.window_size[1] / 2
            )

        if self.is_shaking:
            self.update_shaking_motion()

    def update_shaking_motion(self):
        if self.current_shake_rate:
            self.current_shake_rate -= 1
            self.update_shaking_time()
            return

        self.position.x += randint(0, self.shaking_amount.x) - 4
        self.position.y += randint(0, self.shaking_amount.y) - 4
        self.shaking_timer -= 1

        if self.shaking_timer <= 0:
            self.is_shaking = False

        self.current_shake_rate = self.original_shake_rate

    def update_shaking_time(self):
        self.shaking_timer -= 1

        if self.shaking_timer <= 0:
            self.is_shaking = False

    def shake(
        self, x_amount: int, y_amount: int, frame_duration: int, rate: int = 1
    ) -> None:
        self.current_shake_rate = rate
        self.original_shake_rate = rate
        self.is_shaking = True
        self.shaking_amount = Vector(x_amount, y_amount)
        self.shaking_timer = frame_duration

    @property
    def scroll_in_integer(self) -> Vector:
        int_scroll = self.position.copy()
        int_scroll.x = int(int_scroll.x)
        int_scroll.y = int(int_scroll.y)
        return int_scroll

    def set_target(self, target: Entity):
        self._target = target
