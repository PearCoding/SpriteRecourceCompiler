import os
from PIL import Image
from enum import Enum, unique

@unique
class TileType(Enum):
    Unknown = 0
    Variation = 1
    Frame = 2


""" Simple Tile class holding information """
class Tile:
    x = 0# Final position in sprite package
    y = 0
    variation = 0
    frame = 0

    def __init__(self, file):
        self.image = Image.open(file)
        self.width = self.image.width
        self.height = self.image.height

    def area(self):
        return self.width * self.height

    def size(self):
        return self.width, self.height

    def __repr__(self):
        return 'Tile[' + str(self.width) + ',' + str(self.height) + ']'
