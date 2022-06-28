import pygame

from Engine.Collisions.Collider import Collider
from Engine.Vector import Vector

TILE_SIZE = 20

# TODO: put it in a file
game_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class World:
    collision_tiles: list
    tiles: list

    def __init__(self):
        self.collision_tiles = []
        self.tile_rects = []

    def update(self):
        self.collision_tiles = []
        self.tiles = []

        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == 0:
                    x += 1
                    continue
                self.collision_tiles.append(
                    Collider(Vector(x * TILE_SIZE, y * TILE_SIZE), TILE_SIZE, TILE_SIZE)
                )
                self.tiles.append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
                x += 1
            y += 1

    def draw(self, surface: pygame.Surface, offset: Vector = Vector()):
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == 1:
                    self.draw_tile(surface, Vector(x, y), offset, color=(90, 0, 0))

                if tile == 2:
                    self.draw_tile(surface, Vector(x, y), offset)

                x += 1
            y += 1

    def draw_tile(
        self,
        surface: pygame.Surface,
        position: Vector,
        offset: Vector,
        color: tuple = (50, 50, 150),
    ):
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(
                position.x * TILE_SIZE - offset.x,
                position.y * TILE_SIZE - offset.y,
                TILE_SIZE,
                TILE_SIZE,
            ),
        )
