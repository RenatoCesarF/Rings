import math
from typing import List, Tuple
import pygame
from Engine.Vector import Vector


class Spark:
    position: Vector
    angle: float
    speed: float
    scale: float
    color: Tuple[int, int, int]
    thickness: float
    alive: bool
    points: list

    def __init__(
        self,
        position: Vector,
        angle: float,
        speed: float,
        color: Tuple[int, int, int] = (255, 255, 255),
        scale: float = 1,
        thickness: float = 0.3,
    ) -> None:
        self.position = position
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.thickness = thickness
        self.alive = True
        self.points = []

    def point_towards(self, angle: int, rate) -> None:
        rotate_direction = (
            (angle - self.angle + math.pi * 3) % (math.pi * 2)
        ) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1

        if abs(rotate_direction) < rate:
            self.angle = angle
            return

        self.angle += rate * rotate_sign

    def calculate_movement(self, dt) -> List:
        return [
            math.cos(self.angle) * self.speed * dt,
            math.sin(self.angle) * self.speed * dt,
        ]

    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction

        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt, angle_change=0) -> None:
        movement = self.calculate_movement(dt)
        self.position.x += movement[0]
        self.position.y += movement[1]

        self.angle += angle_change

        # self.point_towards(math.pi/2, 0.02)
        # self.velocity_adjust(0.975,0.2,8,dt)

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surface: pygame.Surface, offset: List[int] = [0, 0]):
        if not self.alive:
            return
        self.points = [
            # Point 1
            [
                self.position.x
                + math.cos(self.angle) * self.speed * self.scale,
                self.position.y
                + math.sin(self.angle) * self.speed * self.scale,
            ],
            # Point 2
            [
                self.position.x
                + math.cos(self.angle + math.pi / 2)
                * self.speed
                * self.scale
                * self.thickness,
                self.position.y
                + math.sin(self.angle + math.pi / 2)
                * self.speed
                * self.scale
                * self.thickness,
            ],
            # Point 3
            [
                self.position.x
                - math.cos(self.angle) * self.speed * self.scale * 3.5,
                self.position.y
                - math.sin(self.angle) * self.speed * self.scale * 3.5,
            ],
            # Point 4
            [
                self.position.x
                + math.cos(self.angle - math.pi / 2)
                * self.speed
                * self.scale
                * self.thickness,
                self.position.y
                - math.sin(self.angle + math.pi / 2)
                * self.speed
                * self.scale
                * self.thickness,
            ],
        ]
        pygame.draw.polygon(surface, self.color, self.points)
