import os
import sys
import subprocess
from .config import (
    BLENDER_BIN, TEMPLATE_PATH,
    EXTRACT_SCRIPT_PATH, MOVIE_SCRIPT_PATH, STEREO_SCRIPT_PATH)


def get_args_from_kwargs(**kwargs):
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


def sequence_to_movie(**kwargs):
    command = [
        BLENDER_BIN,
        TEMPLATE_PATH,
        '--background',
        '--factory-startup',
        '--enable-autoexec',
        '--python', MOVIE_SCRIPT_PATH,
        '--']
    command.extend(get_args_from_kwargs(**kwargs))
    subprocess.call(command)


def extract(**kwargs):
    command = [
        BLENDER_BIN,
        '--background',
        '--factory-startup',
        '--python', EXTRACT_SCRIPT_PATH,
        '--']
    command.extend(get_args_from_kwargs(**kwargs))

    startupinfo = None
    if sys.platform.startswith('win'):
        # Do not pop window when process is called
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(command, startupinfo=startupinfo)


def to_stereo_movie(**kwargs):
    command = [
        BLENDER_BIN,
        '--background',
        '--factory-startup',
        '--python', STEREO_SCRIPT_PATH,
        '--']
    command.extend(get_args_from_kwargs(**kwargs))
    subprocess.call(command)
