from dataclasses import dataclass, field
import math

@dataclass
class Range:
    min: int | float
    max: int | float

    @classmethod
    def fromint(cls, number: int) -> 'Range':
        return Range(number, number)

    def add(self, vrange: 'Range'):
        self.min += vrange.min
        self.max += vrange.max
        return self
    
    def __add__(self, other) -> 'Range':
        if isinstance(other, Range):
            return Range(self.min + other.min, self.max + other.max)
        if isinstance(other, int):
            return Range(self.min + other, self.max + other)
        else:
            raise ValueError("eerm types no good for +")

    def __iadd__(self, other):
        if isinstance(other, Range):
            self.min += other.min
            self.max += other.max
            return self
        if isinstance(other, int):
            self.min += other
            self.max += other
            return self
        else:
            raise ValueError(f"types no good for +\nYou are trying to add {other} to {self}")

    def __mul__(self, other) -> 'Range':
        if isinstance(other, int) or isinstance(other, float):
            return Range(self.min * other, self.max * other)
        else:
            raise ValueError("types no good for *")

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.min *= other
            self.max *= other
        else:
            raise ValueError("types no good for *")
        return self
    
    def floor(self):
        return Range(math.floor(self.min), math.floor(self.max))
    
    def contains(self, x: int | float):
        return x >= self.min and x <= self.max

    def round(self):
        return Range(round(self.min), round(self.max))