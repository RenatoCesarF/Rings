import pygame
from Engine.Vector import Vector
from Engine.Animator.Animation import Animation
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Collisions.Collider import Collider

class Player:
    def __init__(self, position: Vector):
        self.position = position
        self.movement_velocity = Vector()
        self.collision = Collider(position,15,15)
        self.speed = 1
        self.life = 3
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_down = False
        self.is_moving_up = False
        self.is_stand = False
    
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
    
    def update(self,mx, offset: Vector = Vector()):
        self.movement_velocity = Vector()
        self.offset = offset

        self.move()
        self.update_animate(mx)

    def move(self):
        if self.is_moving_left and not self.collision.is_colliding_left:
            self.movement_velocity.x = -1*self.speed        

        if self.is_moving_right and not self.collision.is_colliding_right:
            self.movement_velocity.x = 1*self.speed

        if self.is_moving_up and not self.collision.is_colliding_top:
            self.movement_velocity.y = -1*self.speed
            
        if self.is_moving_down and not self.collision.is_colliding_bottom:
            self.movement_velocity.y = 1*self.speed
        
        self.position.x += self.movement_velocity.x
        self.position.y += self.movement_velocity.y

        self.collision.speed.x = self.movement_velocity.x
        self.collision.speed.y = self.movement_velocity.y
        self.collision.update_position_with_current_speed() 



    def draw(self, surface: pygame.Surface)-> None:
        surface.blit(self.get_frame(),(self.position.x - self.offset.x, self.position.y - self.offset.y))
   

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
