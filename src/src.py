import argparse
import os
import math

from modes import PackMode, PaddingMode
from tile import Tile
from tight_packer import TightPacker
from filter import Filter

from PIL import Image, ImageDraw

APP_NAME = "SpriteResourceCompiler (SRC)"
APP_VERSION = "0.1"


def readable_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a valid path".format(string))
    if os.access(string, os.R_OK):
        return string
    else:
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a readable dir".format(string))


# TODO: Should check if it's possible to write, etc.
def get_file_name(string):
    if os.path.isdir(string):
        raise argparse.ArgumentTypeError("Output:{0} is not a valid path".format(string))
    else:
        return string


def get_pack_mode(string):
    if string.lower() == 'tight':
        return PackMode.Tight
    else:
        return PackMode.VarAnim


def get_padding_mode(string):
    if string.lower() == 'transparent':
        return PaddingMode.Transparent
    elif string.lower() == 'black':
        return PaddingMode.Black
    else:
        return PaddingMode.Fill


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates tilemap from single sprites.')
    parser.add_argument('DIR', type=readable_dir, nargs='+',
                        help='the used directory to search for images')
    parser.add_argument('-o', '--output', dest='output', type=get_file_name, required=True,
                        help='the output file')
    parser.add_argument('-r', '--recursive', dest='recursive', action='store_true',
                        help='search directories and subdirectories recursively')
    parser.add_argument('-f', '--filter', dest='filters', nargs='*',
                        help='add a filter file containing filters for filenames')
    parser.add_argument('-m', '--mode', dest='packmode', type=get_pack_mode,
                        choices=list(PackMode), default=PackMode.Tight,
                        help='the packing mode to use while generating the output')
    parser.add_argument('-p', '--padding', dest='padding', type=int, default=1,
                        help='the padding in pixel between each tile')
    parser.add_argument('-pm', '--padding_mode', dest='padding_mode', type=get_padding_mode, default=PaddingMode.Fill,
                        choices=list(PaddingMode),
                        help='the used algorithm to fill the empty padding gap between each tile')
    parser.add_argument('-p2', '--pow2', dest='pow', action='store_true',
                        help='make the output image size power of 2')
    parser.add_argument('-sqr', '--square', dest='square', action='store_true',
                        help='make the output image size square')
    parser.add_argument('--version', action='version', version='{} {}'.format(APP_NAME, APP_VERSION))

    args = parser.parse_args()

    # Init optional filters
    filter = None
    if args.filters:
        filter = Filter()

        for path in args.filters:
            filter.parse(path)

    # Read image files
    tileFiles = []
    for dir in args.DIR:
        if args.recursive:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    tileFiles.append(os.path.abspath(os.path.join(root, file)))
        else:
            for file in os.listdir(dir):
                tileFiles.append(os.path.abspath(os.path.join(dir, file)))

    tiles = []
    for file in tileFiles:
        try:
            if filter is None or filter.check(os.path.basename(file)):
                tile = Tile(file)
                tiles.append(tile)
        except IOError as e:
            print(e)

    tiles.sort(key=lambda p: p.area())

    if len(tiles) == 0:
        if args.filters:
            print('Nothing to pack. Maybe check filters?')
        else:
            print('Nothing to pack.')
        exit(-1)

    packer = None
    if args.packmode == PackMode.Tight:
        packer = TightPacker(args.padding)
        packer.pack(tiles)
    elif args.packmode == PackMode.VarAnim:
        raise NotImplementedError()

    w, h = packer.size()

    # Setup sizes
    if args.pow:
        w = int(math.pow(2, math.ceil(math.log2(w))))
        h = int(math.pow(2, math.ceil(math.log2(h))))

    if args.square:
        w = max(w, h)
        h = w

    # Draw image:
    image = Image.new("RGBA", (w, h))

    for tile in tiles:
        image.paste(tile.image, (tile.x, tile.y))

    # Fill padding:
    # TODO: Better to encapsulate it in another class
    drawer = ImageDraw.Draw(image)
    padding = args.padding
    black = (0, 0, 0, 255)
    if args.padding_mode != PaddingMode.Transparent:
        for tile in tiles:
            if tile.x > padding:
                if args.padding_mode == PaddingMode.Black:
                    drawer.rectangle((tile.x - padding, tile.y, tile.x - 1, tile.y + tile.height - 1), black)
                else:  # Fill
                    for y in range(tile.y, tile.y + tile.height):
                        pixel = tile.image.getpixel((0, y - tile.y))
                        for x in range(tile.x - padding, tile.x):
                            drawer.point((x, y), pixel)

            if tile.y > padding:
                if args.padding_mode == PaddingMode.Black:
                    drawer.rectangle((tile.x, tile.y - padding, tile.x + tile.width - 1, tile.y - 1), black)
                else:  # Fill
                    for x in range(tile.x, tile.x + tile.width):
                        pixel = tile.image.getpixel((x - tile.x, 0))
                        for y in range(tile.y - padding, tile.y):
                            drawer.point((x, y), pixel)
                    pass

            if tile.x + tile.width < w - 1:  # It's ok to draw over the canvas
                if args.padding_mode == PaddingMode.Black:
                    drawer.rectangle((tile.x + tile.width, tile.y,
                                      tile.x + tile.width + padding - 1, tile.y + tile.height - 1), black)
                else:  # Fill
                    for y in range(tile.y, tile.y + tile.height):
                        pixel = tile.image.getpixel((tile.width - 1, y - tile.y))
                        for x in range(tile.x + tile.width, tile.x + tile.width + padding):
                            drawer.point((x, y), pixel)

            if tile.y + tile.height < h - 1:  # It's ok to draw over the canvas
                if args.padding_mode == PaddingMode.Black:
                    drawer.rectangle((tile.x, tile.y + tile.height,
                                      tile.x + tile.width - 1, tile.y + tile.height + padding - 1), black)
                else:  # Fill
                    for x in range(tile.x, tile.x + tile.width):
                        pixel = tile.image.getpixel((x - tile.x, tile.height - 1))
                        for y in range(tile.y + tile.height, tile.y + tile.height + padding):
                            drawer.point((x, y), pixel)

    print("Output: {} [{}x{}]".format(args.output, image.width, image.height))
    image.save(args.output)