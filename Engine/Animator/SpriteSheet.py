import pygame

class Spritesheet:
    def __init__(self,file_directory: str, scale: int = 1, custom_colorkey = (0,0,0), space_between_sprites: float = 0) -> None:
        self.file_directory = file_directory
        self.sprite_sheet = pygame.image.load(file_directory).convert()
        self.height = self.sprite_sheet.get_height()
        self.width = self.sprite_sheet.get_width()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,(self.width * scale, self.height * scale))
        self.color_key = custom_colorkey
        self.space_between_sprites = space_between_sprites
        self.scale = scale

    def get_sprite(self,x,y,width,height, scale: int = 1, debugging: bool = False) -> pygame.Surface:
        sprite = pygame.Surface((width*self.scale , height* self.scale)) 
        sprite.set_colorkey(self.color_key)
        sprite.blit(self.sprite_sheet,(0,0),(x * self.scale, y * self.scale,
                                             width * self.scale, height * self.scale))
        if debugging:
            pygame.draw.rect(sprite, (200,0,0), pygame.Rect(0,0, width, height), width = 1)

        return sprite
    
    def __str__(self):
        return f"""
            directory: {self.file_directory}
            height: {self.height}
            width: {self.width}
            scale: {self.scale}
        """
