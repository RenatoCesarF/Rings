from __future__ import annotations
import pygame
from pygame import Vector2, display
from Engine.Vector import Vector

from Engine.Animator.Animation import Animation
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Collisions.Collider import Collider

class Player:
    def __init__(self, position: Vector):
        self.position = position
        self.collision = Collider(Vector(0,0),14,14, left_offset=Vector(1,1))
        self.speed = 1
        # self.life = 3
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_down = False
        self.is_moving_up = False
        self.is_stand = False
    
 
    def update(self,mx, tiles: tuple):
        self.move(tiles)
        self.update_animate(mx)

    def move(self, tiles: tuple):
        self.position = Vector()

        if self.is_moving_left:
            self.position.x -= 1*self.speed        

        if self.is_moving_right:
            self.position.x += 1*self.speed

        if self.is_moving_up:
            self.position.y -= 1*self.speed
            
        if self.is_moving_down:
            self.position.y += 1*self.speed

        self.collision.update_position_after_collisions(self.position,tiles)
     
        self.position.x = self.collision.collision_rect.x
        self.position.y = self.collision.collision_rect.y

    def draw(self, surface: pygame.Surface,offset: Vector = Vector(), debugging: bool = False)-> None:
        surface.blit(self.get_frame(),(self.position.x - offset.x, self.position.y - offset.y))
        
        if debugging:
            self.collision.draw_collision_rect(surface, offset, (0,100,0))
   
    def update_animate(self,mx):
        if not self.is_moving_right and not self.is_moving_up  and not self.is_moving_down and not self.is_moving_left:
            if mx > self.position.x:
                self.change_animation(self.idle_right_animation)

            else: self.change_animation(self.idle_left_animation)
        else:
            if mx > self.position.x:
                self.change_animation(self.walking_right_animation)
            else: self.change_animation(self.walking_left_animation)
        
    def change_animation(self,next_animation):
        last_animation = self.current_animation
        self.current_animation = next_animation

        if last_animation != self.current_animation:
            self.current_animation.reset_animation()

    def is_turned_left(self,mx):
        if mx > self.position.x:
            return True
        return False

    def get_frame(self) -> pygame.Surface:
        return self.current_animation.get_next_frame()

    def load_animations(self):
        robot_spritesheet = Spritesheet('res/sprites/robot.png', custom_colorkey = (127,146,255), space_between_sprites=1)

        self.walking_right_animation = Animation(6,speed=self.speed/3)
        self.walking_right_animation.load_from_spritesheet(robot_spritesheet, sprite_height= 14, sprite_width=15,spritesheet_line_height=96)

        self.walking_left_animation = Animation.create_mirrored_animation(self.walking_right_animation)

        self.idle_right_animation = Animation(24,speed=self.speed/3)
        self.idle_right_animation.load_from_spritesheet(robot_spritesheet,sprite_height= 14,sprite_width=17, spritesheet_line_height= 49)
        self.idle_right_animation.append_animation_from_same_spritesheet(2, spritesheet_line_height=64)

        self.idle_left_animation = Animation.create_mirrored_animation(self.idle_right_animation)
        self.current_animation = self.walking_left_animation
   