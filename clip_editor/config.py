import os
import sys

current_dir = os.path.dirname(__file__)
current_dir = os.path.normpath(current_dir)

TEMPLATE_PATH = os.path.join(current_dir, 'template.blend')
PROCESS_SCRIPT_PATH = os.path.join(current_dir, 'process.py')
EXTRACT_SCRIPT_PATH = os.path.join(current_dir, 'extract.py')

if sys.platform.startswith('linux'):
    BLENDER_BIN = 'blender'
    FFMPEG_BIN = 'ffmpeg'
else:
    BLENDER_BIN = 'blender.exe'
    FFMPEG_BIN = 'ffmpeg.exe'
