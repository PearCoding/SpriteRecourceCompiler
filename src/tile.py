import os
from PIL import Image
from enum import Enum, unique

from modes import PackMode


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

    def __init__(self, file, mode):
        self.image = Image.open(file)

    def area(self):
        return self.image.width * self.image.height

    def size(self):
        return self.image.width, self.image.height

    def __repr__(self):
        return 'Tile[' + str(self.image.width) + ',' + str(self.image.height) + ']'
