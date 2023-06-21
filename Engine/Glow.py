from typing import Tuple
import pygame


class Glow:
    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        color: Tuple[int, int, int] = (0, 0, 0),
        radius: int = 0,
    ):
        self.radius = radius
        self.color = color
        self.width = width
        self.height = height

    def circle_glow(self) -> pygame.Surface:
        surf = pygame.Surface(
            (self.width * 2, self.height * 2)
        )  # self.radius*2, self.radius*2))

        # pygame.draw.circle(surf,self.color, (self.radius,self.radius), 20)

        pygame.draw.rect(
            surf,
            self.color,
            pygame.Rect(self.width / 2, self.height / 2, self.width, self.height),
            width=0,
            border_radius=self.radius,
        )

        surf.set_colorkey((0, 0, 0))
        return surf

    def __str__(self):
        return f"""
            radius: {self.radius}
            color: {self.color}
            width: {self.width}
            height: {self.height}
        """
