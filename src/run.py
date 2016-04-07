import argparse
import os

from modes import PackMode


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
    elif string == 'var_anim_tight':
        return PackMode.VarAnimTight
    else:
        return PackMode.VarAnim


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates tilemap from single sprites.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('DIRS', type=readable_dir, nargs='+',
                        help='Input directories')
    parser.add_argument('-o', '--output', type=argparse.FileType("wb"), required=True,
                        help='The output file')
    parser.add_argument('-p', '--pack', type=get_pack_mode,
                        choices=['var_anim', 'var_anim_tight', 'tight'], default='var_anim',
                        help='The packing mode to use.')

    args = parser.parse_args()
    #TODO