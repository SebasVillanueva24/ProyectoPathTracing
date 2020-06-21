from Point import *

class Ray:
    pos = Point(0,0)
    source = Point(0,0)

    def __init__(self, pos, source):
        self.pos = pos
        self.source = source
