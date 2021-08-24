import pygame

class Spritesheet:
    def __init__(self,file_directory: str) -> None:
        self.file_directory = file_directory
        self.sprite_sheet = pygame.image.load(file_directory).convert()
    
    def get_sprite(self,x,y,width,height, debugging: bool = False) -> pygame.Surface:
        sprite = pygame.Surface((width,height))
        sprite.set_colorkey((0,213,255))
        sprite.blit(self.sprite_sheet,(0,0),(x,y,width,height))

        if not debugging:
            return sprite

        pygame.draw.rect(sprite, (200,0,0), pygame.Rect(0,0, width, height), width = 1)
        return sprite
