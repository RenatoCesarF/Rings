import pygame
import pygame


class Window:
    screen: any
    screen_real_size: tuple
    base_screen_size: tuple
    display: pygame.Surface

    def __init__(self, configs: dict, is_mouse_visible: bool = False):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(32)
        pygame.display.set_caption("Rings")
        pygame.mouse.set_visible(is_mouse_visible)
        self.base_screen_size = configs["resolution"]
        self.screen_real_size = (300, 200)

        self.screen = pygame.display.set_mode(
            (self.base_screen_size[0], self.base_screen_size[1]), 0, 32
        )

        self.display = pygame.Surface((300, 200))

    def blit_displays(self):
        self.screen.blit(
            pygame.transform.scale(self.display, self.base_screen_size),
            (
                (self.screen.get_width() - self.base_screen_size[0]) // 2,
                (self.screen.get_height() - self.base_screen_size[1]) // 2,
            ),
        )
