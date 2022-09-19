from typing import Tuple
from pygame.surface import Surface
import pygame


class Spritesheet:
    def __init__(
        self,
        file_directory: str,
        scale: int = 1,
        custom_colorkey: Tuple[int, int, int]=(0, 0, 0),
        space_between_sprites: int = 0,
    ) -> None:
        """Load a spritesheet image by the file_directory and apply the custom_colorkey to it.
           if your animation has a space between the sprites, you can configure it as well.

        Args:
            `file_directory` (str): The path to the spritesheet image
            `scale` (int, optional): Apply a scale into all your spritesheet. Defaults to 1.
            `custom_colorkey` (tuple, optional): Apply this colorkey to all the sprite. Defaults to (0,0,0).
            `space_between_sprites` (float, optional): If your spritesheet has a space between the frames,
                                    you need to configure this, obs: this space will be applyed to the first sprite as well. Defaults to 0.
        """
        self.file_directory: str = file_directory
        self.image: Surface = pygame.image.load(file_directory).convert()
        self.height: int = self.image.get_height()
        self.width: int = self.image.get_width()
        self.image = pygame.transform.scale(
            self.image, (self.width * scale, self.height * scale)
        )
        self.color_key: Tuple[int, int, int] = custom_colorkey
        self.space_between_sprites: int = space_between_sprites
        self.scale: int = scale

    def get_sprite(
        self, x: int, y: int, width: int, height: int, debugging: bool = False
    ) -> pygame.Surface:
        """Return a pygame Surface with the sprite in the x,y position and with this width and height.

        Args:
            `x` (int): X position inside the spritesheet where the sprite is
            `y` (int): Y position inside the spritesheet where the sprite is
            `width` (int): width of the sprite
            `height` (int): height of the sprite
            `debugging` (bool, optional): If is debugging or not. Sometimes it helps to se where the sprite actule is.
                ` Defaults` to False.

        Returns:
            pygame.Surface: You can use it to blit into some pygame.surface
        """
        sprite: Surface = pygame.Surface((width * self.scale, height * self.scale))
        sprite.set_colorkey(self.color_key)
        sprite.blit(
            self.image,
            (0, 0),
            (x * self.scale, y * self.scale, width * self.scale, height * self.scale),
        )
        if debugging:
            pygame.draw.rect(
                sprite, (200, 0, 0), pygame.Rect(0, 0, width, height), width=1
            )

        return sprite

    def __str__(self) -> str:
        return f"""
            directory: {self.file_directory}
            height: {self.height}
            width: {self.width}
            scale: {self.scale}
        """
