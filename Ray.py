from Point import *

class Ray:

    pos = Point(0,0)
    source = Point(0,0)
    dir = source - pos

    def __init__(self, pos, source):
        self.pos = pos
        self.source = source
        self.dir = source - pos
