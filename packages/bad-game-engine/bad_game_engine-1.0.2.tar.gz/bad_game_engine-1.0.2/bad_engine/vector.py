from __future__ import annotations
from math import sqrt

class Vector:
    def __init__(self, x:float, y:float) -> None:
        """
        a simple vector class for positions
        """

        self.x = float(x)
        self.y = float(y)
    
    def distance(self, other:Vector) -> float:
        x = self.x - other.x
        y = self.y - other.y
        
        i = x**2+y**2
        i = sqrt(i)

        return i

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y) 
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y) 
    
    def __floordiv__(self, other):
        return Vector(self.x // other.x, self.y // other.y)
    
    def __truediv__(self, other):
        return Vector(self.x / other.x, self.y / other.y)
    
    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)

    def __pow__(self, other):
        return Vector(self.x ** other.x, self.y ** other.y)

    def __repr__(self):
        pos = (self.x, self.y)
        return f"{pos}"