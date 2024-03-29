from typing import List
import pygame
import json
from Engine.Collisions.Collider import Collider
from Engine.Window import Window
from Engine.image import Image
from Engine.Vector import Vector
from Engine.Config import TILE_HEIGHT, TILE_SIZE, TILE_WIDTH
from Engine.World.Tile import Tile

game_map = json.load(open('test.json'))
MAP_OFFSET: Vector = Vector(5, 1)


class World:
    """The class that controll, draw and administrate the world map"""

    collision_tiles: List[Collider]
    vertical_map_size: int
    horizontal_map_size: int
    map_matrix: List[List[Tile]]

    def __init__(self):
        self.collision_tiles = []
        self.tile_rects = []
        self.map_matrix = game_map
        self.vertical_map_size = len(game_map)
        self.horinzontal_map_size = len(game_map[0])
        self.test_image: Image = Image(
            './res/sprites/ground6.png', (215, 123, 186)
        )
        self.create_world_tiles()

    def create_world_tiles(self):
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                t = Tile(
                    position=Window.to_isometric_position(x, y),
                    size=TILE_WIDTH,
                    grid_index=Vector(x, y),
                    content=tile,
                )
                self.map_matrix[y][x] = t
                x += 1
            y += 1

    def draw_grid(self, surface, offset: Vector):
        for i in range(0, self.vertical_map_size):
            for j in range(0, self.horinzontal_map_size):
                t = Tile(
                    Vector(i * TILE_WIDTH, j * TILE_HEIGHT),
                    TILE_WIDTH,
                    content=4,
                    thikness=1,
                    grid_index=Vector(i, j),
                )
                t.draw(surface, offset)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface, offset: Vector = Vector.zero()):
        for row in game_map:
            for tile in row:
                if tile.content == 0:
                    continue
                self.test_image.draw(surface, tile.position, offset)

    @staticmethod
    def get_tile_position_in_grid(
        position: Vector, camera_position: Vector
    ) -> Vector:
        # get the mouse offset position inside the tile
        offset = Vector(position.x % TILE_SIZE.x, position.y % TILE_SIZE.y)
        # Add camera_position scroll to offset
        offset.x += camera_position.x % TILE_SIZE.x
        offset.y += camera_position.y % TILE_SIZE.y

        cell_position = Vector(
            (position.x // TILE_SIZE.x), (position.y // TILE_SIZE.y)
        )
        # Add camera_position scroll to cell
        cell_position.x += int(camera_position.x // TILE_SIZE.x)
        cell_position.y += int(camera_position.y // TILE_SIZE.y)

        # get the selected cell in iso grid
        selected_pos = Vector(
            (cell_position.y - MAP_OFFSET.y)
            + (cell_position.x - MAP_OFFSET.x),
            (cell_position.y - MAP_OFFSET.y)
            - (cell_position.x - MAP_OFFSET.x),
        )

        # height and width of a quarter of a tile,
        #  select the corner of the tile to nodge to a direction
        h, w = TILE_SIZE.y / 2, TILE_SIZE.x / 2
        if offset.y < (h / w) * (w - offset.x):
            selected_pos.x -= 1
        if offset.y > (h / w) * offset.x + h:
            selected_pos.y += 1
        if offset.y < (h / w) * offset.x - h:
            selected_pos.y -= 1
        if offset.y > (h / w) * (2 * w - offset.x) + h:
            selected_pos.x += 1

        # translate the selected cell to world coordinate
        return Vector(selected_pos.x, selected_pos.y)

    def is_tile_position_valid(self, x: int, y: int) -> bool:
        if y < 0 or x < 0:
            return False
        if x >= self.horinzontal_map_size or y >= self.vertical_map_size:
            return False

        tile = self.map_matrix[y][x]

        if tile.content == 0:
            return False

        return True
