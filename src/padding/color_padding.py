from padding.padding import Padding

from PIL import ImageDraw


class ColorPadding(Padding):
    def __init__(self, color=(0, 0, 0, 255)):
        self.color = color

    def fill(self, img, tiles, padding):
        drawer = ImageDraw.Draw(img)
        for tile in tiles:
            if tile.x > padding:
                drawer.rectangle((tile.x - padding, tile.y,
                                  tile.x - 1, tile.y + tile.height - 1), self.color)

            if tile.y > padding:
                drawer.rectangle((tile.x, tile.y - padding,
                                  tile.x + tile.width - 1, tile.y - 1), self.color)

            if tile.x + tile.width < img.width - 1:  # It's ok to draw over the canvas
                drawer.rectangle((tile.x + tile.width, tile.y,
                                  tile.x + tile.width + padding - 1, tile.y + tile.height - 1), self.color)

            if tile.y + tile.height < img.height - 1:  # It's ok to draw over the canvas
                drawer.rectangle((tile.x, tile.y + tile.height,
                                  tile.x + tile.width - 1, tile.y + tile.height + padding - 1), self.color)