from Engine.Vector import Vector
import pygame


class Mouse:
    true_position: Vector
    position: Vector
    image: any

    def __init__(self, window):
        self.window = window
        self.true_position = Vector()
        self.position = Vector()
        self.image = pygame.transform.scale(
            pygame.image.load("res/mouse.png").convert(), (44, 44)
        )
        self.image.set_colorkey((255, 0, 0))

    def update(self, tick=30):
        self.position.x, self.position.y = pygame.mouse.get_pos()
        self.true_position.x = self.position.x
        self.true_position.y = self.position.y

        self.position.x -= (
            self.window.screen.get_width() - self.window.base_screen_size[0]
        ) // 3
        self.position.y -= (
            self.window.screen.get_height() - self.window.base_screen_size[1]
        ) // 3

        self.position.x /= self.window.base_screen_size[0] / self.window.display.get_width()
        self.position.y /= (
            self.window.base_screen_size[1] / self.window.display.get_height()
        )

    def draw(self, surface: pygame.Surface):
        surface.blit(
            self.image,
            (
                self.true_position.x // 3 * 3 - self.image.get_width() / 2,
                self.true_position.y // 3 * 3 - self.image.get_height() / 2,
            ),
        )
