from typing import List


from pygame.surface import Surface
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
        self.unit_list.append(unit)
        self.unit_list = sorted(self.unit_list,key= lambda x:x.position.y)
        