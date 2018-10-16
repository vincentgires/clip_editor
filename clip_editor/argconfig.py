import sys
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-input',
        help='File input',
        required=True)
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
        required=True)
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
        '-output',
        help='File output',
        required=True)

    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args