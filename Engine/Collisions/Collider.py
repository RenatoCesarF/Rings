from __future__ import annotations
from typing import List, Tuple
import pygame

from Engine.Vector import Vector


class Collider:
    def __init__(
        self,
        initial_position: Vector,
        width: int,
        height: int,
        collision_tolerance: int = 3,
        left_offset: Vector = Vector.zero(),
    ) -> None:
        self.collision_rect = pygame.Rect(
            initial_position.x, initial_position.y, width, height
        )
        self.left_offset = (
            left_offset  # TODO: implement a way to add offset to collision
        )
        self.collision_tolerance = collision_tolerance
        self.speed = Vector.zero()
        self.width = width
        self.height = height

        self.is_active = True
        self.is_colliding = False
        self.is_colliding_top = False
        self.is_colliding_bottom = False
        self.is_colliding_left = False
        self.is_colliding_right = False

    def check_multiple_tiles_collision(
        self, tile_list: List[Collider]
    ) -> List[Collider]:
        colide_list: List[Collider] = []

        for tile in tile_list:
            if self.collision_rect.colliderect(tile.collision_rect):
                colide_list.append(tile)
        return colide_list

    def update_position_after_check_collisions(
        self, next_position: Vector, tiles: List[Collider]
    ) -> None:
        self.reset_all_collisions()
        self.collision_rect.x += next_position.x
        hit_list = self.check_multiple_tiles_collision(tiles)

        for tile in hit_list:
            if next_position.x > 0:
                self.collision_rect.right = tile.collision_rect.left
                self.is_colliding_right = True
            elif next_position.x < 0:
                self.collision_rect.left = tile.collision_rect.right
                self.is_colliding_left = True

        self.collision_rect.y += next_position.y
        hit_list = self.check_multiple_tiles_collision(tiles)

        for tile in hit_list:
            if next_position.y > 0:
                self.collision_rect.bottom = tile.collision_rect.top
                self.is_colliding_bottom = True
            elif next_position.y < 0:
                self.collision_rect.top = tile.collision_rect.bottom
                self.is_colliding_top = True

    def draw_collision_rect(
        self,
        destination_surface: pygame.Surface,
        offset: Vector = Vector.zero(),
        color: Tuple[int, int, int] = (250, 0, 0),
        width: int = 1,
    ) -> None:
        pygame.draw.rect(
            destination_surface,
            color,
            pygame.Rect(
                self.collision_rect.x - offset.x,  # + self.left_offset.x,
                self.collision_rect.y - offset.y,  # + self.left_offset.y,
                self.width,
                self.height,
            ),
            width=width,
        )

    def reset_all_collisions(self) -> None:
        self.is_colliding = False
        self.is_colliding_top = False
        self.is_colliding_bottom = False
        self.is_colliding_left = False
        self.is_colliding_right = False

    # def check_single_collising_with(self, other_collider: Collider) -> None:
    #     if not self.is_active:
    #         self.reset_all_collisions()
    #         return
    #     if not self.collision_rect.colliderect(other_collider.collision_rect):
    #         self.reset_all_collisions()
    #         return

    #     self.is_colliding = True

    #     self.__check_sides_collisition(other_collider)

    # def __check_sides_collisition(self,other_collider: Collider) -> None:
    #     distance_between_top_bottom = abs(other_collider.collision_rect.top - self.collision_rect.bottom)
    #     distance_between_bottom_top = abs(other_collider.collision_rect.bottom - self.collision_rect.top)
    #     distance_between_right_left = abs(other_collider.collision_rect.right - self.collision_rect.left)
    #     distance_between_left_right = abs(other_collider.collision_rect.left - self.collision_rect.right)

    #     if  distance_between_top_bottom < self.collision_tolerance and self.speed.y > 0:
    #         self.is_colliding_bottom = True
    #     if distance_between_bottom_top < self.collision_tolerance and self.speed.y < 0:
    #         self.is_colliding_top = True
    #     if distance_between_right_left < self.collision_tolerance and self.speed.x < 0:
    #         self.is_colliding_left = True
    #     if  distance_between_left_right < self.collision_tolerance and self.speed.x > 0:
    #         self.is_colliding_right = True
