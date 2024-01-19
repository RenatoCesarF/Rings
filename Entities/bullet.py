from __future__ import annotations

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from Engine.Entity import Entity
from Engine.Vector import Vector


class Bullet(Entity):
    position: Vector
    target: Entity
    direction: Vector
    speed: float
    alive: bool
    collision_rect: Rect

    def __init__(self, position: Vector, target: Entity, speed: float = 1):
        self.position = position
        self.target = target
        self.direction = Vector.zero()
        self.speed = speed
        self.alive = True
        self.collision_rect = Rect(position.x, position.y, 5, 5)

    def update(self):
        if not self.alive or not self.target:
            return
        self.direction.x = self.target.position.x - self.position.x
        self.direction.y = self.target.position.y - self.position.y

        self.direction = self.direction.normalize()
        self.position.x += int(self.direction.x * self.speed)
        self.position.y += int(self.direction.y * self.speed)
        self.collision_rect.x = self.position.x - 2
        self.collision_rect.y = self.position.y - 2

        if (
            not self.target.collision_rect
            or self.target.collision_rect is None
        ):
            print('target has no collision rect')
            return

        self.handle_target_collision()

    def handle_target_collision(self):
        if not self.collided_with_target():
            return
        self.alive = False

    def collided_with_target(self):
        if self.collision_rect.colliderect(self.target.collision_rect):
            return True
        return False

    def draw(self, surface: Surface, offset: Vector = Vector.zero()):
        if not self.alive or not self.target:
            return
        render_pos = (self.position.x - offset.x, self.position.y - offset.y)
        pygame.draw.circle(surface, (200, 0, 0), render_pos, 3)
        pygame.draw.circle(surface, (255, 255, 255), render_pos, 2)
        # draw_collision_rect(self.collision_rect, surface, offset)
