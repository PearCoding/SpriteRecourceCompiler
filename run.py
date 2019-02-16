import argparse
import math
import os

from PIL import Image, PILLOW_VERSION
import src

APP_NAME = "SpriteResourceCompiler (SRC)"


def readable_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError(
            "{0} is not a valid path".format(string))
    if os.access(string, os.R_OK):
        return string
    else:
        raise argparse.ArgumentTypeError(
            "{0} is not a readable dir".format(string))


# TODO: Should check if it's possible to write, etc.
def get_file_name(string):
    if os.path.isdir(string):
        raise argparse.ArgumentTypeError(
            "{0} is not a valid path".format(string))
    else:
        return string


def get_pack_mode(string):
    if string.lower() == 'tight':
        return src.PackMode.Tight
    else:
        raise argparse.ArgumentTypeError(
            "{0} is not a valid mode".format(string))


def get_padding_mode(string):
    if string.lower() == 'transparent':
        return src.PaddingMode.Transparent
    elif string.lower() == 'black':
        return src.PaddingMode.Black
    elif string.lower() == 'white':
        return src.PaddingMode.White
    elif string.lower() == 'magenta':
        return src.PaddingMode.Magenta
    elif string.lower() == 'fill':
        return src.PaddingMode.Fill
    else:
        raise argparse.ArgumentTypeError(
            "{0} is not a valid mode".format(string))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generates tilemap from single sprites.')
    parser.add_argument('DIR', type=readable_dir, nargs='+',
                        help='the used directory to search for images')
    parser.add_argument('-o', '--output', dest='output', type=get_file_name, required=True,
                        help='the output file')
    parser.add_argument('-l', '--list', dest='csv', type=get_file_name,
                        help='optional csv file output with the positions of every sprite')
    parser.add_argument('-dl', '--datalisp', dest='dl', type=get_file_name,
                        help='optional datalisp file with the positions and name of every sprite')
    parser.add_argument('-r', '--recursive', dest='recursive', action='store_true',
                        help='search directories and subdirectories recursively')
    parser.add_argument('-f', '--filter', dest='filter', nargs='*',
                        help='add a filter for filenames (wildcard)')
    parser.add_argument('-ff', '--filter-file', dest='filterfile', nargs='*',
                        help='add a filter file containing filters for filenames (wildcard)')
    parser.add_argument('-x', dest='processorfile', nargs='*',
                        help='add a processor xml file containing rules to process given sprites')
    parser.add_argument('-m', '--mode', dest='packmode', type=get_pack_mode,
                        choices=list(src.PackMode), default=src.PackMode.Tight,
                        help='the packing mode to use while generating the output')
    parser.add_argument('-p', '--padding', dest='padding', type=int, default=1,
                        help='the padding in pixel between each tile')
    parser.add_argument('-pm', '--padding_mode', dest='padding_mode', type=get_padding_mode, default=src.PaddingMode.Fill,
                        choices=list(src.PaddingMode),
                        help='the used algorithm to fill the empty padding gap between each tile')
    parser.add_argument('-p2', '--pow2', dest='pow', action='store_true',
                        help='make the output image size power of 2')
    parser.add_argument('-sqr', '--square', dest='square', action='store_true',
                        help='make the output image size square')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='draw debug information as well (DEBUG)')
    parser.add_argument('--version', action='version', version='{0} {1} with PILLOW {2}'.format(
        APP_NAME, src.VERSION_STR, PILLOW_VERSION))

    args = parser.parse_args()

    # Init optional filters
    filter = src.Filter()
    if args.filter or args.filterfile:
        for case in args.filter:
            filter.add(case)

        for path in args.filterfile:
            filter.parse(path)
    else:
        filter = src.get_standard_filter()

    # 1. Read image files
    tileFiles = []
    for dir in args.DIR:
        if args.recursive:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    if filter.check(os.path.basename(file)):
                        tileFiles.append(os.path.abspath(
                            os.path.join(root, file)))
        else:
            for file in os.listdir(dir):
                if filter.check(os.path.basename(file)):
                    tileFiles.append(os.path.abspath(os.path.join(dir, file)))

    # 2. Processor

    tiles = []
    if args.processorfile and len(args.processorfile) > 0:
        processor = src.Processor()
        for file in args.processorfile:
            parser = src.Parser()
            parser.from_file(file)
            parser.parse(processor)
        outputs = processor.execute(tileFiles)
        for output in outputs:
            tiles.append(src.Tile(output.name, output.file, True))
    else:
        for file in tileFiles:
            try:
                tile = src.Tile("_unknown_", file)
                tiles.append(tile)
            except IOError as e:
                print(e)

    tiles.sort(key=lambda p: p.area(), reverse=True)

    if len(tiles) == 0:
        print('Nothing to pack. Maybe check filters?')
        exit(-1)

    # 4. Pack files
    packer = None
    if args.packmode == src.PackMode.Tight:
        packer = src.TightPacker(args.padding)
        packer.pack(tiles)
    elif args.packmode == src.PackMode.VarAnim:
        raise NotImplementedError()

    # Get sizes (Better recalculate it)
    w = 0
    h = 0

    for tile in tiles:
        if w < tile.x + tile.width + args.padding*2:
            w = tile.x + tile.width + args.padding*2
        if h < tile.y + tile.height + args.padding*2:
            h = tile.y + tile.height + args.padding*2

    w -= args.padding*2
    h -= args.padding*2
    print(w, h)

    # Setup sizes
    if args.pow:
        w = int(math.pow(2, math.ceil(math.log(w, 2))))
        h = int(math.pow(2, math.ceil(math.log(h, 2))))

    if args.square:
        w = max(w, h)
        h = w

    # Draw image:
    def_color = 0
    if args.padding_mode == src.PaddingMode.Black:
        def_color = (0, 0, 0, 255)
    elif args.padding_mode == src.PaddingMode.White:
        def_color = (255, 255, 255, 255)
    elif args.padding_mode == src.PaddingMode.Magenta:
        def_color = (255, 0, 255, 255)

    image = Image.new("RGBA", (w, h), def_color)

    for tile in tiles:
        image.paste(tile.image, (tile.x, tile.y))

    # 5. Fill padding:
    if args.padding > 0 and args.padding_mode != src.PaddingMode.Transparent:
        padder = None
        # if args.padding_mode == PaddingMode.Black:
        #    padder = ColorPadding()
        # elif args.padding_mode == PaddingMode.White:
        #    padder = ColorPadding((255, 255, 255, 255))
        # elif args.padding_mode == PaddingMode.Magenta:
        #    padder = ColorPadding((255, 0, 255, 255))
        if args.padding_mode == src.PaddingMode.Fill:
            padder = src.FillPadding()

        if padder:
            padder.fill(image, tiles, args.padding)

    print("Output: {0} [{1}x{2}]".format(
        args.output, image.width, image.height))
    image.save(args.output)

    if args.csv:
        src.CSVWriter.write(args.csv, tiles)

    if args.dl:
        src.DLWriter.write(args.dl, tiles)
