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

    def area(self):
        return self.w * self.h


class TightPacker(Packer):
    def __init__(self, padding):
        self.padding = padding
        self.w, self.h = 0, 0
        self.freeRects = []

    def sort_free_rects(self):
        self.freeRects = sorted(self.freeRects, key=lambda rect: rect.area())

    def enlarge_area(self, tile):
        self.freeRects.append(FreeRect(self.w+self.padding*2, 0,
                                       tile.width, self.h))
        self.freeRects.append(FreeRect(0, self.h+self.padding*2,
                                       self.w, tile.width))
        self.freeRects.append(FreeRect(self.w+self.padding*2, self.h + self.padding*2,
                                       tile.width, tile.height))
        self.sort_free_rects()

        self.w += tile.width + self.padding*2
        self.h += tile.height + self.padding*2

    def find_area(self, tile):
        for area in self.freeRects:
            if area.fit(tile):
                return area
        return None

    def pack(self, tiles):
        queue = deque(tiles)

        first = queue.popleft()
        first.x = 0
        first.y = 0

        self.w, self.h = first.size()

        while len(queue) > 0:
            tile = queue.popleft()
            area = self.find_area(tile)
            if area is None:
                #TODO: First try to merge some free rects together!
                self.enlarge_area(tile)
                area = self.find_area(tile)

            tile.x = area.x
            tile.y = area.y
            self.freeRects.remove(area)

    def size(self):
        return self.w, self.h
