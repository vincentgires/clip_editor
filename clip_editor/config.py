import os
import sys

current_dir = os.path.dirname(__file__)
current_dir = os.path.normpath(current_dir)

TEMPLATE_PATH = os.path.join(current_dir, 'template.blend')
SCRIPT_PATH = os.path.join(current_dir, 'process.py')

if sys.platform.startswith('linux'):
    BLENDER_BIN = '/nwave/software/Blender/2.79a/linux64/blender'
    FFMPEG_BIN = '/nwave/software/FFmpeg/4.0/linux64/ffmpeg'
else:
    BLENDER_BIN = '//nwave/software/Blender/2.79a/win64/blender.exe'
    FFMPEG_BIN = '//nwave/software/FFmpeg/4.0/win64/bin/ffmpeg.exe'
