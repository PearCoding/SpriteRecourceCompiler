from packer import Packer
from collections import deque


class FreeRect:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def fit(self, tile):
        tw, th = tile.size()
        return (tw <= self.w) and (th <= self.h)


class TightPacker(Packer):
    def __init__(self):
        self.w, self.h = 0, 0
        self.freeRects = []

    def enlargeArea(self, tile):
        pass#TODO: Add this!

    def findArea(self, tile):
        for area in self.freeRects:
            if area.fit(tile):
                return area
        return None

    def pack(self, tiles, padding):
        queue = deque(tiles)

        first = queue.popleft()
        first.x = 0
        first.y = 0

        self.w, self.h = first.size()

        while len(queue) > 0:
            tile = queue.popleft()
            area = self.findArea(tile)
            if area is None:
                self.enlargeArea(tile)
                area = self.findArea(tile)

            tile.x = area.x
            tile.y = area.y
            self.freeRects.remove(area)

    def size(self):
        return self.w, self.h
