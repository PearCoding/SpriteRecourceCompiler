import argparse
import os
import math

from modes import PackMode
from tile import Tile

from tight_packer import TightPacker


def readable_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a valid path".format(string))
    if os.access(string, os.R_OK):
        return string
    else:
        raise argparse.ArgumentTypeError("ReadableDir:{0} is not a readable dir".format(string))


def get_pack_mode(string):
    if string == 'tight':
        return PackMode.Tight
    else:
        return PackMode.VarAnim


def area_sort(p):
    return p.area()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates tilemap from single sprites.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('DIRS', type=readable_dir, nargs='+',
                        help='Input directories')
    parser.add_argument('-o', '--output', dest='output', type=argparse.FileType("wb"), required=True,
                        help='The output file')
    parser.add_argument('-m', '--mode', dest='packmode', type=get_pack_mode,
                        choices=['var_anim', 'tight'], default='tight',
                        help='The packing mode to use.')
    parser.add_argument('-p', '--padding', dest='padding', type=int, default=1,
                        help='The padding between each tile.')
    parser.add_argument('-p2', '--pow2', dest='pow',
                        help='Make the width and height of the output image power of 2.')
    parser.add_argument('-sqr', '--square', dest='square',
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
    print(tiles)

    if args.packmode == PackMode.Tight:
        packer = TightPacker()
        packer.pack(tiles, args.padding)
    elif args.packmode == PackMode.VarAnim:
        raise NotImplementedError()

    w, h = packer.size()

    # Setup sizes
    if args.pow:
        w = math.pow(2, math.ceil(math.log2(w)))
        h = math.pow(2, math.ceil(math.log2(h)))

    if args.square:
        w = max(w, h)
        h = w

    # Draw image:
