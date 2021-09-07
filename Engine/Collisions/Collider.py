
#TODO: A way to rewrite the function solve_colision() maybe @overwrite

from __future__ import annotations
import pygame

from Engine.Vector import Vector

class  Collider:
    def __init__(self, initial_position: Vector, width: int, height: int, collision_tolerance: int = 10) -> None:
        self.collision_rect = pygame.Rect(initial_position.x,initial_position.y,width, height)
        self.collision_tolerance = collision_tolerance
        self.speed = Vector()
        self.width = width
        self.height = height

        self.is_active = True
        self.is_colliding = False
        self.is_colliding_top = False
        self.is_colliding_bottom = False
        self.is_colliding_left = False
        self.is_colliding_right = False
     
    # def is_colliding(self) -> bool:
    #     return self.is_colliding_bottom or self.is_colliding_left or self.is_colliding_top or self.is_colliding_right
    
    def check_colliding_with(self, other_collider: Collider) -> None:
        if not self.is_active:
            self.set_all_collisiont_to_false()
            return
        if not self.collision_rect.colliderect(other_collider.collision_rect):
            self.set_all_collisiont_to_false()
            return

        self.is_colliding = True

        self.__check_sides_collisition(other_collider)


    def __check_sides_collisition(self,other_collider: Collider):
        distance_between_top_bottom = abs(other_collider.collision_rect.top - self.collision_rect.bottom)
        distance_between_bottom_top = abs(other_collider.collision_rect.bottom - self.collision_rect.top)
        distance_between_right_left = abs(other_collider.collision_rect.right - self.collision_rect.left)
        distance_between_left_right = abs(other_collider.collision_rect.left - self.collision_rect.right)

        if  distance_between_top_bottom < self.collision_tolerance and self.speed.y > 0:
            self.is_colliding_top = True
        if distance_between_bottom_top < self.collision_tolerance and self.speed.y < 0:
            self.is_colliding_bottom = True
        if distance_between_right_left < self.collision_tolerance and self.speed.x < 0:
            self.is_colliding_right = True
        if  distance_between_left_right < self.collision_tolerance and self.speed.x > 0:
            self.is_colliding_left = True

        
    # def update_position(self) -> None:
    #     self.collision_rect.x += self.speed.x
    #     self.collision_rect.y += self.speed.y

    def draw_collision_rect(self, destination_surface: pygame.Surface, color: tuple = (250,0,0), width: int = 1) -> None:
        pygame.draw.rect(destination_surface, color, pygame.Rect(self.collision_rect.x,self.collision_rect.y,self.width,self.height), width=width)

    def set_all_collisiont_to_false(self):
        self.is_colliding = False
        self.is_colliding_top = False
        self.is_colliding_bottom = False
        self.is_colliding_left = False
        self.is_colliding_right = False
        
        