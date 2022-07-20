import pygame
import json
from Engine.Collisions.Collider import Collider
from Engine.Vector import Vector
from Engine.World.Tile import Tile

TILE_SIZE = 20


game_map = json.load(open("test.json"))


class World:
    collision_tiles: list
    tiles: list

    def __init__(self):
        self.collision_tiles = []
        self.tile_rects = []

    def update(self):
        self.collision_tiles = []
        self.tiles: Dict[Tile] = []

        y = 0
        # TODO: put it in a file

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
                    Tile(
                        position=Vector(x * TILE_SIZE, y * TILE_SIZE),
                        size=TILE_SIZE,
                        color_index=tile,
                    )
                )
                x += 1
            y += 1

    def draw(self, surface: pygame.Surface, offset: Vector = Vector()):
        for tile in self.tiles:
            tile.draw(surface, offset)
