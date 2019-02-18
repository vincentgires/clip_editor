import sys
import argparse


def _arg_to_keyvalue(arg):
    """Convert argument to key/value pair.

    -textoverlay position=800,600
    -textoverlay position=TOP_LEFT
    """

    k, v = arg.split('=')
    if ',' in v:
        v = tuple(float(c) for c in v.split(','))
    else:
        v = v.upper()
    return (k, v)


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
        help='Resolution X Y',
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
        action='append',
        nargs='+',
        type=_arg_to_keyvalue)

    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args


def args_from_kwargs(**kwargs):
    """Convert kwargs into parsable arguments.

    -key value_a value_b
    """

    result = []
    for k in kwargs:
        arg = kwargs[k]
        if isinstance(arg, list):
            result.append('-{}'.format(k))
            result.extend([str(f) for f in arg])
        else:
            result.extend(['-{}'.format(k), str(arg)])
    return result
