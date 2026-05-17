# Practice special methods in Python classes (dunder = double underscore function)

from __future__ import annotations

import math


class Vector:
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        # Instance-level attributes
        self.x = x
        self.y = y
        
    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"
    
    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)
    
    def __bool__(self) -> bool:
        return bool(abs(self))
    
    # Method creates and returns a new instance of Vector and
    # does not modify self.
    def __add__(self, other: Vector) -> Vector:
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
    
    def __mul__(self, scalar: int) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)
    
v1 = Vector(1, 1)
v2 = Vector(2, 2)

print(f"V1: {v1}")
print(f"V2: {v2}")
print(f"V1 +  V2: {v1 + v2}")
print(f"Bool V2: {bool(v2)}")
print(f"Multiply V2 * 2: {v2 * 2}")
print(f"Representation of V1 (repr): {repr(v1)}")