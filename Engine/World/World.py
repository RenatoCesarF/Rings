from typing import List
import pygame
import json
from Engine.Collisions.collider import Collider
from Engine.vector import Vector
from Engine.config import TILE_SIZE
from Engine.World.Tile import Tile

game_map = json.load(open("test.json"))

class World:
    collision_tiles: List[Collider]
    tiles: List[Tile]
    vertical_map_size: int
    horizontal_map_size: int

    def __init__(self):
        self.collision_tiles = []
        self.tile_rects = []
        self.vertical_map_size = len(game_map[0])
        self.horinzontal_map_size = len(game_map)
        
    def draw_grid(self, surface, offset: Vector):
        for i in range (0, self.vertical_map_size):
            for j in range(0 , self.horinzontal_map_size):
                t = Tile(Vector(i* TILE_SIZE, j * TILE_SIZE),
                        TILE_SIZE,
                        content=4, thikness=1)
                t.draw(surface, offset)

    def update(self):
        # self.collision_tiles = []
        self.tiles: List[Tile] = []

        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == 0:
                    x += 1
                    continue

                # self.collision_tiles.append(
                #     Collider(Vector(x * TILE_SIZE, y * TILE_SIZE), TILE_SIZE, TILE_SIZE)
                # )
                self.tiles.append(
                    Tile(
                        position=self.get_isometric_tile_position(x,y),
                        size=TILE_SIZE,
                        content=tile,
                    )
                )
                x += 1
            y += 1
            
    def get_isometric_tile_position(self, x: int, y: int) -> Vector:
        y_offset = (0.25 *TILE_SIZE.y)
        x_offset = (0.5 *TILE_SIZE.x)
        return Vector(
            x * x_offset + y * -x_offset,
            x * y_offset + y * y_offset
        )
        
    def draw(self, surface: pygame.Surface, offset: Vector = Vector()):
        for tile in self.tiles:
            tile.draw(surface, offset)
