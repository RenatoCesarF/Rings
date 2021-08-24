import pygame

class Spritesheet:
    def __init__(self,file_directory: str, scale: int = 1) -> None:
        self.file_directory = file_directory
        self.sprite_sheet = pygame.image.load(file_directory).convert()
        self.height = self.sprite_sheet.get_height()
        self.width = self.sprite_sheet.get_width()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,(self.width * scale, self.height * scale))
        self.scale = scale

    def get_sprite(self,x,y,width,height, scale: int = 1, debugging: bool = False) -> pygame.Surface:
        sprite = pygame.Surface((width*self.scale , height* self.scale)) 
        sprite.set_colorkey((0,213,255))
        sprite.blit(self.sprite_sheet,(0,0),(x * self.scale, y * self.scale,
                                             width * self.scale, height * self.scale))
        if debugging:
            pygame.draw.rect(sprite, (200,0,0), pygame.Rect(0,0, width, height), width = 1)

        return sprite
