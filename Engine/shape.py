from enum import Enum


class Shape(Enum):
    Rect = 1
    Box = 2
    Circle = 3
    Polygon = 4

    def __str__(self):
        return f""" 
            Rect -> 1
            Box -> 2
            Circle -> 3
            Polygon -> 4
        """
