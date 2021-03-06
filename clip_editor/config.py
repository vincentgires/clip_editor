import os
import sys

_current_dir = os.path.dirname(__file__)
_current_dir = os.path.normpath(_current_dir)

BLENDER_FOLDER_PATH = os.path.join(_current_dir, 'blender')
BLENDER_SCRIPTS_PATH = os.path.join(BLENDER_FOLDER_PATH, 'scripts')
TEMPLATE_PATH = os.path.join(BLENDER_FOLDER_PATH, 'template.blend')
PROCESS_SCRIPT_PATH = os.path.join(BLENDER_SCRIPTS_PATH, 'process.py')
EXTRACT_SCRIPT_PATH = os.path.join(BLENDER_SCRIPTS_PATH, 'extract.py')
STEREO_SCRIPT_PATH = os.path.join(BLENDER_SCRIPTS_PATH, 'stereo.py')
MOVIE_SCRIPT_PATH = os.path.join(
    BLENDER_SCRIPTS_PATH, 'movie.py')

if sys.platform.startswith('win'):
    BLENDER_BIN = 'blender.exe'
    FFMPEG_BIN = 'ffmpeg.exe'
else:
    BLENDER_BIN = 'blender'
    FFMPEG_BIN = 'ffmpeg'
