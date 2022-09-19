from __future__ import annotations
from typing import Any
import pygame
from pygame.surface import Surface
from Engine.vector import Vector

from Engine.Animator.animation import Animation
from Engine.Animator.spriteSheet import Spritesheet
from Engine.Collisions.collider import Collider
from Engine.entity import Entity

class Player(Entity):
    game: Any
    position: Vector
    collision: Collider
    speed: int

    def __init__(self, game: Any) -> None:
        self.game = game
        self.position = Vector()
        self.collision = Collider(Vector(0, 0), 14, 14, left_offset=Vector(1, 1))
        self.speed = 1
        # self.life = 3
        self.is_moving_left: bool = False
        self.is_moving_right: bool = False
        self.is_moving_down: bool = False
        self.is_moving_up: bool = False
        self.is_stand: bool = False

    def update(self) -> None:
        self.is_not_walking: bool = (
            not self.is_moving_right
            and not self.is_moving_up
            and not self.is_moving_down
            and not self.is_moving_left
        )
        self.move()
        self.update_animate()

    def move(self) -> None:
        self.position = Vector()

        if self.is_moving_left:
            self.position.x -= 1 * self.speed

        if self.is_moving_right:
            self.position.x += 1 * self.speed

        if self.is_moving_up:
            self.position.y -= 1 * self.speed

        if self.is_moving_down:
            self.position.y += 1 * self.speed

        self.collision.update_position_after_check_collisions(
            self.position, self.game.world.collision_tiles
        )
        self.position.x = self.collision.collision_rect.x
        self.position.y = self.collision.collision_rect.y

    def update_animate(self) -> None:
        is_turned_left: bool = (
            self.game.mouse.position.get_copy().x
            > self.position.x - self.game.camera.position.get_copy().x
        )
        is_not_moving: bool = (
            not self.is_moving_right
            and not self.is_moving_up
            and not self.is_moving_down
            and not self.is_moving_left
        )
        if is_not_moving:
            if is_turned_left:
                self.change_animation(self.idle_right_animation)
                return

            self.change_animation(self.idle_left_animation)
            return

        if is_turned_left:
            self.change_animation(self.walking_right_animation)
            return

        self.change_animation(self.walking_left_animation)

    def draw(self, surface: pygame.Surface, offset: Vector = Vector()) -> None:
        surface.blit(
            self.get_frame(),
            (self.position.x - offset.x, self.position.y - offset.y),
        )

    def change_animation(self, next_animation: Animation) -> None:
        last_animation: Animation = self.current_animation
        self.current_animation: Animation = next_animation

        if last_animation != self.current_animation:
            self.current_animation.reset_animation()

    def get_frame(self) -> Surface:
        return self.current_animation.get_next_frame()

    def load_animations(self):
        robot_spritesheet: Spritesheet = Spritesheet(
            "res/sprites/robot.png",
            custom_colorkey=(127, 146, 255),
            space_between_sprites=1,
        )

        self.walking_right_animation: Animation = Animation(6, speed=self.speed / 3)
        self.walking_right_animation.load_from_spritesheet(
            robot_spritesheet,
            sprite_height=14,
            sprite_width=15,
            spritesheet_line_height=96,
        )

        self.walking_left_animation: Animation = Animation.create_mirrored_animation(
            self.walking_right_animation
        )

        self.idle_right_animation: Animation = Animation(24, speed=self.speed / 3)
        self.idle_right_animation.load_from_spritesheet(
            robot_spritesheet,
            sprite_height=14,
            sprite_width=17,
            spritesheet_line_height=49,
        )
        self.idle_right_animation.append_animation_from_same_spritesheet(
            2, spritesheet_line_height=64
        )

        self.idle_left_animation: Animation = Animation.create_mirrored_animation(
            self.idle_right_animation
        )
        self.current_animation = self.walking_left_animation
