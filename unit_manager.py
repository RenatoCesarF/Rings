from typing import List


from pygame.surface import Surface
from Engine.World.tile import Tile
from Engine.image import Image
from Engine.timer import Timer
from Engine.vector import Vector

from Engine.window import Window

from Entities.unit import Unit

class UnitManager:
    window: Window
    unit_list: List[Unit]
    time_to_add_unit: Timer
    time_to_remove_unit: Timer
    selected_unit: Unit
    def __init__(self, window):
        self.selected_unit = None
        self.window = window
        self.unit_list = []
        self.time_to_add_unit = Timer(500, True)
        self.time_to_remove_unit = Timer(500, True)

    def draw(self, surface: Surface, offset: Vector):
        for unit in self.unit_list:
            unit.draw(surface, offset)
        
        self.draw_selected_unit(surface, offset)
 
    def draw_selected_unit(self, surface: Surface, offset: Vector) -> None:
        if not self.selected_unit:
            return
        
        self.selected_unit.tower_img.draw_outline(
            surface,
            self.selected_unit.screen_position,
            offset
        )
        self.selected_unit.draw(surface, offset)
       
 
    def update(self, delta):
        self.time_to_add_unit.update_timer(delta)
        self.time_to_remove_unit.update_timer(delta)
        
    def add_unit_to_list(self, unit: Unit):
        if (
            self.is_tile_position_occupied(unit.tile_position) 
            or not self.time_to_add_unit.has_finished()
        ): 
            return
        unit.unique_id = len(self.unit_list)
        self.unit_list.append(unit)
        self.unit_list = sorted(self.unit_list,key= lambda x:x.screen_position.y)
        self.time_to_add_unit.reset()

    def remove(self, to_remove: Unit) -> bool:
        if not self.time_to_remove_unit.has_finished():
            return
        self.time_to_remove_unit.reset()
        for unit in self.unit_list:
            if unit == to_remove:
                self.unit_list.remove(unit)
                return True
        return False
                
    def get_unit_at_position(self, position: Vector, offset: Vector = Vector()) -> Unit:
        for unit in sorted(self.unit_list,key= lambda x:x.screen_position.y *-1):
            if unit.collision_rect.collidepoint(
                position.x + offset.x,
                position.y + offset.y
            ):
                return unit
            
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