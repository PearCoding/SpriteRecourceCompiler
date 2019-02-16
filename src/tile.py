from PIL import Image


class Tile:
    """ Simple Tile class holding information """

    def __init__(self, name, file, raw=False):
        if raw:
            self.image = file
        else:
            self.image = Image.open(file)
        self.name = name
        self.width = self.image.width
        self.height = self.image.height
        self.x = -1
        self.y = -1

    def area(self):
        return self.width * self.height

    def size(self):
        return self.width, self.height

    def is_set(self):
        return self.x >= 0 and self.y >= 0

    def __repr__(self):
        return 'Tile[' + str(self.width) + ',' + str(self.height) + ']'
