import os
import sys
import subprocess
from .config import (
    BLENDER_BIN, EXTRACT_SCRIPT_PATH, MOVIE_SCRIPT_PATH, STEREO_SCRIPT_PATH)


def _get_args_from_kwargs(**kwargs):
    '''Convert kwargs into parsable arguments.
    "-key value_a value_a"
    '''
    result = []
    for k in kwargs:
        arg = kwargs[k]
        if isinstance(arg, list):
            result.append('-{}'.format(k))
            result.extend([str(f) for f in arg])
        else:
            result.extend(['-{}'.format(k), str(arg)])
    return result


def _call_blender(script_path, **kwargs):
    command = [
        BLENDER_BIN,
        '--background',
        '--factory-startup',
        '--enable-autoexec',
        '--python', script_path,
        '--']
    command.extend(_get_args_from_kwargs(**kwargs))
    startupinfo = None
    if sys.platform.startswith('win'):
        # Do not pop window when process is called
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(command, startupinfo=startupinfo)


def sequence_to_movie(**kwargs):
    _call_blender(script=MOVIE_SCRIPT_PATH)


def extract(**kwargs):
    _call_blender(script=EXTRACT_SCRIPT_PATH)


def to_stereo_movie(**kwargs):
    _call_blender(script=STEREO_SCRIPT_PATH)
