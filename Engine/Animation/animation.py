import pygame
from Engine.Animation.SpriteSheet import Spritesheet
class Animation:
    def __init__(self, frames_amount: int, speed: float = 1, time: float = 1) -> None:
        self.frames = []
        self.frames_amount = frames_amount
        self.speed = speed
        self.current_frame = 0
        self.time = time
        self.initial_animation_time = time

    def load_from_spritesheet(self, sprite_sheet: Spritesheet, sprite_width: float,
                          sprite_height: float, line_height: float) -> None:
        for i in range(self.frames_amount):
            self.frames.append(sprite_sheet.get_sprite(sprite_width*(i), line_height, sprite_width, sprite_height))

    def get_next_frame(self) -> pygame.Surface:
        if self.current_frame >= self.frames_amount:
            self.current_frame = 0
        current = self.current_frame
        self.time -= self.speed
        if self.time <= 0:
            self.time = self.initial_animation_time
            
            self.current_frame +=1

        return self.frames[current]