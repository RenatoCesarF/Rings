from typing import List


from pygame.surface import Surface
from Engine.World.tile import Tile
from Engine.image import Image
from Engine.vector import Vector

from Engine.window import Window

from unit import Unit

class UnitManager:
    window: Window
    unit_list: List[Unit]
    def __init__(self, window):
        self.window = window
        self.unit_list = []

    def draw(self, surface: Surface, offset: Vector):
        for unit in self.unit_list:
            unit.draw(surface, offset)
        
    def add_unit_to_list(self, unit: Unit):
        if self.is_tile_position_occupied(unit.tile_position):
            return
        unit.unique_id = len(self.unit_list)
        self.unit_list.append(unit)
        self.unit_list = sorted(self.unit_list,key= lambda x:x.screen_position.y)

    def is_tile_position_occupied(self, tile_position: Vector) -> bool:
        for unit in self.unit_list:
            if (
                unit.tile_position.x == tile_position.x 
                and unit.tile_position.y == tile_position.y
            ) :
                return True
        
        return False
        
    def get_unit_in_tile(self, tile_x, tile_y) -> Unit:
        for unit in self.unit_list:
            if (
                unit.tile_position.x == tile_x
                and unit.tile_position.y == tile_y
            ):
                return unit
        return None