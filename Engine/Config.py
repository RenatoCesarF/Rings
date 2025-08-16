import json
from typing import Any, Dict, Tuple, List

from Engine.Vector import Vector

TILE_SIZE = Vector(28, 14)
TILE_WIDTH = 28
TILE_HEIGHT = 14


class Config:
    debugging: bool = False
    json: Dict[str, Any]
    resolution: List[int]

    def __init__(self, path_to_config_file: str):
        self.json = json.load(open(path_to_config_file))
        self.resolution = self.json.get('resolution')
        debug = self.json.get('debug')
        self.debugging = debug if debug is not None else False

    def resolution_as_tuple(self) -> Tuple[int, int]:
        """Return the game window resolution in the tuple format"""
        return (self.resolution[0], self.resolution[1])

config = Config("./res/config.json")
