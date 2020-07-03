from Point import *

class Segment:
    a = Point(0,0)
    b = Point(0,0)
    tipo = ""
    vertical = False

    def __init__(self, a, b, tipo,vertical):
        self.a = a
        self.b = b
        self.tipo = tipo
        self.vertical = vertical


