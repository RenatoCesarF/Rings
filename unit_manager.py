from typing import List

from pygame.surface import Surface

from Engine.timer import Timer
from Engine.vector import Vector

from Entities.unit import Unit
from Entities.bullet import Bullet


class UnitManager:
    unit_list: List[Unit]
    time_to_add_unit: Timer
    time_to_remove_unit: Timer
    selected_unit: Unit
    bullets: List[Bullet]

    def __init__(self):
        self.selected_unit = None
        self.unit_list = []
        self.bullets = []
        self.time_to_add_unit = Timer(0, True)
        self.time_to_remove_unit = Timer(500, True)

    def draw(self, surface: Surface, offset: Vector):
        for unit in self.unit_list:
            unit.draw(surface, offset)
        for bullet in self.bullets:
            bullet.draw(surface, offset)
        self.draw_selected_unit(surface, offset)

    def draw_selected_unit(self, surface: Surface, offset: Vector) -> None:
        if not self.selected_unit:
            return

        self.selected_unit.draw_fire_range(surface, offset)
        self.selected_unit.tower_img.draw_outline(
            surface, self.selected_unit.screen_position, offset
        )
        self.selected_unit.draw(surface, offset)

    def update(self, delta):
        self.time_to_add_unit.update_timer(delta)
        self.time_to_remove_unit.update_timer(delta)

        for unit in self.unit_list:
            unit.update()

        for i, b in enumerate(self.bullets):
            b.update()
            if not b.alive:
                self.bullets.pop(i)

    def add_unit_to_list(self, unit: Unit):
        if (
            self.is_tile_position_occupied(unit.tile_position)
            or not self.time_to_add_unit.has_finished()
        ):
            return
        unit.unique_id = len(self.unit_list)
        self.unit_list.append(unit)
        self.unit_list = sorted(self.unit_list, key=lambda x: x.screen_position.y)
        self.time_to_add_unit.reset()

    def remove(self, to_remove: Unit) -> bool:
        if not self.time_to_remove_unit.has_finished():
            return False
        self.time_to_remove_unit.reset()
        for unit in self.unit_list:
            if unit == to_remove:
                self.unit_list.remove(unit)
                return True
        return False

    def get_unit_at_position(self, position: Vector, offset: Vector = Vector()) -> Unit:
        for unit in sorted(self.unit_list, key=lambda x: x.screen_position.y * -1):
            if unit.collision_rect.collidepoint(
                position.x + offset.x, position.y + offset.y
            ):
                return unit
        return None  # Unit(Vector(-1, -1), None)

    def is_tile_position_occupied(self, tile_position: Vector) -> bool:
        for unit in self.unit_list:
            if (
                unit.tile_position.x == tile_position.x
                and unit.tile_position.y == tile_position.y
            ):
                return True

        return False

    def get_unit_in_tile(self, tile_x, tile_y) -> Unit:
        for unit in self.unit_list:
            if unit.tile_position.x == tile_x and unit.tile_position.y == tile_y:
                return unit
        return None
