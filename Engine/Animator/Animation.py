from __future__ import annotations
from typing import List
import pygame
from pygame.surface import Surface
from Engine.Animator.SpriteSheet import Spritesheet
from Engine.Vector import Vector


class Animation:
    def __init__(
        self,
        frames_amount: int,
        speed: float = 1,
        time: float = 1,
        is_debugging: bool = False,
    ) -> None:
        """A single animation that can be loaded from a spritesheet, you need to setup a frames amount to start it.
            Int the future it will be possible to initialize an animation a folder instead of a spritesheet

        Args:
            `frames_amount` (int): The amount of frames dãh.
            `speed` (float, optional): The velocity that your time will pass each frame. Defaults to 1.
            `time` (float, optional): how many frames does last your animation. Defaults to 1.
            `is_debugging` (bool, optional): if setted to True, a red square will be drawn around the frames.
                            Defaults to False.
        """
        self.frames: List[Surface] = []
        self.frames_amount: int = frames_amount
        self.speed: float = speed
        self.is_debugging: bool = is_debugging
        self.current_frame = 0
        self.time: float = time
        self.initial_animation_time: float = time

    def load_from_spritesheet(
        self,
        sprite_sheet: Spritesheet,
        sprite_width: int,
        sprite_height: int,
        spritesheet_line_height: int,
        isReverse: bool = False,
    ) -> None:
        """Load/create an animation from a spritesheet

        Args:
            `sprite_sheet` (Spritesheet): An Spritesheet object already created
            `sprite_width` (float): the width of the sprite animation, this value is used in get_sprite with the spritesheet
            `sprite_height` (float):  the width of the sprite animation, this value is used in get_sprite with the spritesheet
            `spritesheet_line_height` (float): the Y position of your animation inside the spritesheet, the first Y pixel
            `isReverse` (bool, optional): Is setted as True the animation will get 80% more frames and will play foward and backwards
        """
        self.sprite_height = sprite_height
        self.spritesheet = sprite_sheet
        self.sprite_width = sprite_width

        space_between_sprites: int = sprite_sheet.space_between_sprites
        sprite_width += space_between_sprites

        for i in range(self.frames_amount):
            sprite_position = Vector(
                int(sprite_width * (i) + space_between_sprites),
                spritesheet_line_height,
            )
            self.frames.append(
                sprite_sheet.get_sprite(
                    sprite_position.x,
                    sprite_position.y,
                    sprite_width - space_between_sprites,
                    sprite_height,
                    debugging=self.is_debugging,
                )
            )
        if not isReverse:
            return

        for i in range(self.frames_amount - 1, 1, -1):
            self.frames.append(
                sprite_sheet.get_sprite(
                    sprite_width * (i),
                    spritesheet_line_height,
                    sprite_width,
                    sprite_height,
                    debugging=self.is_debugging,
                )
            )
        self.frames_amount += self.frames_amount - 3

    def reset_animation(self) -> None:
        """Returns the animation to the first frame"""
        self.current_frame = 0

    def get_next_frame(self) -> Surface:
        """Returns the next frame of the animation, each time you call it, it returns the next frame of this animation

        Returns:
            pygame.Surface: The image of the frame it self to be blited into another surface
        """
        # TODO a way to reset the animation when change from one to another
        if self.current_frame >= self.frames_amount:
            self.current_frame = 0

        current: int = self.current_frame
        self.time -= self.speed

        if self.time <= 0:
            self.time = self.initial_animation_time

            self.current_frame += 1

        return self.frames[current]

    def append_two_animations(self, animation: Animation) -> None:
        """Attach another animation in the end of this animation if self by using another animation
            You can do the same thing with `append_animation_from_same_spritesheet()` without need to create
            another animation.

        Args:
            animation (Animation): The animmation to be attached
        """
        for frame in animation.frames:
            self.frames.append(frame)
        self.frames_amount += animation.frames_amount

    def append_animation_from_same_spritesheet(
        self,
        frame_amount: int,
        spritesheet_line_height: float,
        custom_width: int = 0,
        custom_height: int = 0,
    ) -> None:
        """Attach more frames into this animation using the same spritesheet that this one was loaded from.
            This is used to add animations that get too big to fit in one line of the spritesheet

        Args:
            frame_amount (int): how many frames will be added
            spritesheet_line_height (float): The Y value of the first pixel of the animation,
                                    the height where it is in the SS
            custom_width (int, optional): If the sprite to be added had a different width of the original one. Defaults to None.
            custom_height (int, optional): If the sprite to be added had a different height of the original one. Defaults to None.
        """
        if not custom_height and not custom_width:
            custom_height = self.sprite_height
            custom_width = self.sprite_width

        space_between_sprites = self.spritesheet.space_between_sprites
        self.frames_amount += frame_amount

        custom_width += space_between_sprites
        for i in range(frame_amount):
            sprite_position = Vector(
                int(custom_width * (i) + space_between_sprites),
                int(spritesheet_line_height),
            )
            self.frames.append(
                self.spritesheet.get_sprite(
                    sprite_position.x,
                    sprite_position.y,
                    custom_width - space_between_sprites,
                    custom_height,
                    debugging=self.is_debugging,
                )
            )

    @classmethod
    def create_mirrored_animation(
        cls,
        animation: Animation,
        horizontally: bool = True,
        vertically: bool = False,
    ) -> Animation:
        """Returns a new animation that is a mirrored version of passed in the args. This is
            a class method, so it only can be used with `Animation.create_mir...`. Usally the
            mirrored animations are only horizontally, but you can inverse it as you want,
            vertical or horizontally

        Args:
            animation (Animation): The base animation to me merrored
            horizontally (bool, optional): If `True` mirrored the animation in the X axis. Defaults to `True`.
            vertically (bool, optional):  If `True` mirrored the animation in the Y axis
                        turning upsidedown. Defaults to False.

        Returns:
            Animation: type Anumation and can be attached to a new animation without the need to configure
        """
        mirroredAnimation: Animation = Animation(
            animation.frames_amount,
            animation.speed,
            animation.initial_animation_time,
        )
        mirroredAnimation.frames = animation.frames.copy()
        for index, frame in enumerate(mirroredAnimation.frames):
            mirroredAnimation.frames[index] = pygame.transform.flip(
                frame, horizontally, vertically
            )

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
