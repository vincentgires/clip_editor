import os
import sys

current_dir = os.path.dirname(__file__)
current_dir = os.path.normpath(current_dir)

SCRIPTS_PATH = os.path.join(current_dir, 'scripts')
TEMPLATE_PATH = os.path.join(SCRIPTS_PATH, 'template.blend')
PROCESS_SCRIPT_PATH = os.path.join(SCRIPTS_PATH, 'process.py')
EXTRACT_SCRIPT_PATH = os.path.join(SCRIPTS_PATH, 'extract.py')

if sys.platform.startswith('linux'):
    BLENDER_BIN = 'blender'
    FFMPEG_BIN = 'ffmpeg'
else:
    BLENDER_BIN = 'blender.exe'
    FFMPEG_BIN = 'ffmpeg.exe'
