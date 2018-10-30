import sys
import argparse
import json


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-inputs',
        nargs='+',
        help='File input',
        required=False)
    parser.add_argument(
        '-inputpath',
        help='Path',
        required=False)
    parser.add_argument(
        '-startframe',
        type=int,
        help='Start frame to begin the clip',
        required=False)
    parser.add_argument(
        '-frames',
        nargs='+',
        type=int,
        help='List of frames to render',
        required=False)
    parser.add_argument(
        '-croptop',
        type=int,
        help='Crop top',
        required=False)
    parser.add_argument(
        '-cropbottom',
        type=int,
        help='Crop bottom',
        required=False)
    parser.add_argument(
        '-fps',
        type=int,
        help='FPS',
        required=False)
    parser.add_argument(
        '-resolution',
        nargs='+',
        type=int,
        help='-resolution X Y',
        required=False)
    parser.add_argument(
        '-colordepth',
        help='Color depth',
        required=False)
    parser.add_argument(
        '-colorspace',
        help='Footage colorspace',
        required=False)
    parser.add_argument(
        '-viewtransform',
        help='OCIO View Transform',
        required=False)
    parser.add_argument(
        '-output',
        help='File output',
        required=False)
    parser.add_argument(
        '-debug',
        help='Debug',
        required=False)
    parser.add_argument(
        '-textoverlay',
        type=json.loads,
        help='Overlay in a JSON Dump format',
        required=False)

    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args
