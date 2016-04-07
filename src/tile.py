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
    variation = 0
    frame = 0

    def __init__(self, path, mode):
        self.image = Image.open(path)

        if mode != PackMode.Tight:
            name = os.path.splitext(path)[0]
            #TODO: Add parser for filenames.

