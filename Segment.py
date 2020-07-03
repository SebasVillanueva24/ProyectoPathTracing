from Point import *

class Segment:
    a = Point(0,0)
    b = Point(0,0)
    especular = False
    vertical = False

    def __init__(self, a, b, especular,vertical):
        self.a = a
        self.b = b
        self.especular = especular
        self.vertical = vertical


