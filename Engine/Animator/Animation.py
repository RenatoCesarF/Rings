from __future__ import annotations
import pygame
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Vector import Vector
class Animation:
    def __init__(self, frames_amount: int, speed: float = 1, time: float = 1, is_debugging: bool = False) -> None:
        self.frames = []
        self.frames_amount = frames_amount
        self.speed = speed
        self.is_debugging = is_debugging
        self.current_frame = 0
        self.time = time
        self.initial_animation_time = time


    def load_from_spritesheet(self, sprite_sheet: Spritesheet, sprite_width: float,
                          sprite_height: float, spritesheet_line_height: float, isReverse: bool = False) -> None:
        self.sprite_height = sprite_height
        self.spritesheet = sprite_sheet
        self.sprite_width = sprite_width
        space_between_sprites = sprite_sheet.space_between_sprites
        sprite_width +=space_between_sprites

        for i in range(self.frames_amount):
            sprite_position = Vector((sprite_width*(i)+ space_between_sprites), spritesheet_line_height)
            self.frames.append(sprite_sheet.get_sprite(sprite_position.x, sprite_position.y,
                               sprite_width - space_between_sprites, sprite_height, debugging = self.is_debugging))
        if not isReverse:
            return

        for i in range(self.frames_amount-1,1,-1):
            self.frames.append(sprite_sheet.get_sprite(sprite_width*(i), spritesheet_line_height, 
                               sprite_width, sprite_height, debugging = debugging))
        self.frames_amount +=self.frames_amount - 3

    def get_next_frame(self) -> pygame.Surface:
        if self.current_frame >= self.frames_amount:
            self.current_frame = 0

        current = self.current_frame
        self.time -= self.speed

        if self.time <= 0:
            self.time = self.initial_animation_time
            
            self.current_frame +=1

        return self.frames[current]
        
    def append_animation_with_animation(self, animation: Animation) -> None:
        for frame in animation.frames:
            self.frames.append(frame)
        self.frames_amount += animation.frames_amount

    def append_animation_from_same_spritesheet(self,frame_amount: int, spritesheet_line_height: float,
                                               custom_width: int = None, custom_height: int = None) -> None:
                                               #TODO: make documentation about all functions
        if custom_height is None and custom_width is None:
            custom_height = self.sprite_height
            custom_width = self.sprite_width

        space_between_sprites = self.spritesheet.space_between_sprites
        self.frames_amount += frame_amount

        custom_width += space_between_sprites
        for i in range(frame_amount):
            sprite_position = Vector((custom_width*(i)+ space_between_sprites), spritesheet_line_height)
            self.frames.append(self.spritesheet.get_sprite(sprite_position.x, sprite_position.y,
                               custom_width - space_between_sprites, custom_height, debugging = self.is_debugging))

    @classmethod
    def createMirroredAnimation(cls, animation: Animation, horizontaly: bool = True, vertically: bool = False) -> Animation:
        mirroredAnimation = Animation(animation.frames_amount,animation.speed,animation.initial_animation_time)
        mirroredAnimation.frames = animation.frames.copy()
        for index, frame in enumerate(mirroredAnimation.frames):
            mirroredAnimation.frames[index] = pygame.transform.flip(frame,horizontaly,vertically)

        return mirroredAnimation

    def __str__(self) -> str:
        return f"""
            frames lenght: {len(self.frames)}
            frame amount: {self.frames_amount}
            speed: {self.speed}
            current frame: {self.current_frame}
            time: {self.time}
            initial animation time: {self.initial_animation_time}
        """