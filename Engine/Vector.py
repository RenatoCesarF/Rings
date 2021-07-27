
class Vector2D():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self