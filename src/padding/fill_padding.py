from .padding import Padding

from PIL import ImageDraw


class FillPadding(Padding):
    def fill(self, img, tiles, padding):
        drawer = ImageDraw.Draw(img)
        for tile in tiles:
            if tile.x > padding:
                for y in range(tile.y, tile.y + tile.height):
                    pixel = tile.image.getpixel((0, y - tile.y))
                    for x in range(tile.x - padding, tile.x):
                        drawer.point((x, y), pixel)

            if tile.y > padding:
                for x in range(tile.x, tile.x + tile.width):
                    pixel = tile.image.getpixel((x - tile.x, 0))
                    for y in range(tile.y - padding, tile.y):
                        drawer.point((x, y), pixel)

            if tile.x + tile.width < img.width - 1:  # It's ok to draw over the canvas
                for y in range(tile.y, tile.y + tile.height):
                    pixel = tile.image.getpixel((tile.width - 1, y - tile.y))
                    for x in range(tile.x + tile.width, tile.x + tile.width + padding):
                        drawer.point((x, y), pixel)

            if tile.y + tile.height < img.height - 1:  # It's ok to draw over the canvas
                for x in range(tile.x, tile.x + tile.width):
                    pixel = tile.image.getpixel((x - tile.x, tile.height - 1))
                    for y in range(tile.y + tile.height, tile.y + tile.height + padding):
                        drawer.point((x, y), pixel)
