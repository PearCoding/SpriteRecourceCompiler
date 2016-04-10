import argparse
import os
import math

from modes import PackMode, PaddingMode
from tile import Tile
from tight_packer import TightPacker

from PIL import Image, ImageDraw


def readable_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a valid path".format(string))
    if os.access(string, os.R_OK):
        return string
    else:
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a readable dir".format(string))


def get_file_name(string):
    if os.path.isdir(string):
        raise argparse.ArgumentTypeError("Output:{0} is not a valid path".format(string))
    else:
        return string


def get_pack_mode(string):
    if string == 'tight':
        return PackMode.Tight
    else:
        return PackMode.VarAnim


def get_padding_mode(string):
    if string == 'transparent':
        return PaddingMode.Transparent
    elif string == 'black':
        return PaddingMode.Black
    else:
        return PaddingMode.Fill


def area_sort(p):
    return p.area()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates tilemap from single sprites.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('DIRS', type=readable_dir, nargs='+',
                        help='Input directories')
    parser.add_argument('-o', '--output', dest='output', type=get_file_name, required=True,
                        help='The output file')
    parser.add_argument('-m', '--mode', dest='packmode', type=get_pack_mode,
                        choices=list(PackMode), default=PackMode.Tight,
                        help='The packing mode to use.')
    parser.add_argument('-p', '--padding', dest='padding', type=int, default=1,
                        help='The padding between each tile.')
    parser.add_argument('-pm', '--padding_mode', dest='padding_mode', type=get_padding_mode, default=PaddingMode.Fill,
                        choices=list(PaddingMode),
                        help='The used algorithm to fill the padding between each tile.')
    parser.add_argument('-p2', '--pow2', dest='pow', action='store_true',
                        help='Make the width and height of the output image power of 2.')
    parser.add_argument('-sqr', '--square', dest='square', action='store_true',
                        help='Make output image square.')

    args = parser.parse_args()
    tiles = []
    for dir in args.DIRS:
        for file in os.listdir(dir):
            try:
                tile = Tile(os.path.abspath(dir + "/" + file), args.packmode)
                tiles.append(tile)
            except IOError as e:
                print(e)

    tiles.sort(key=area_sort)

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

            if tile.x + tile.width < w - padding:
                if args.padding_mode == PaddingMode.Black:
                    drawer.rectangle((tile.x + tile.width, tile.y,
                                      tile.x + tile.width + padding - 1, tile.y + tile.height - 1), black)
                else:  # Fill
                    for y in range(tile.y, tile.y + tile.height):
                        pixel = tile.image.getpixel((tile.width - 1, y - tile.y))
                        for x in range(tile.x + tile.width, tile.x + tile.width + padding):
                            drawer.point((x, y), pixel)

            if tile.y + tile.height < h - padding:
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
